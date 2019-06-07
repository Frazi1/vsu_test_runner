﻿using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Runtime.Serialization;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using BusinessLayer.Executors;
using BusinessLayer.Executors.PipelineTasks;
using BusinessLayer.Validators;
using BusinessLayer.Wildcards;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;
using SharedModels.Enum;
using Utils;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class CodeService : BaseService
    {
        private readonly ExecutorsProvider _executorsProvider;
        private readonly CodeSnippetRepository _codeSnippetRepository;
        private readonly WildcardsFactory _wildcardsFactory;
        private readonly TestingInputRepository _testingInputRepository;
        private readonly ValidationService _validationService;

        public CodeService(
            ICurrentUser currentUser,
            ExecutorsProvider executorsProvider,
            CodeSnippetRepository codeSnippetRepository,
            WildcardsFactory wildcardsFactory,
            TestingInputRepository testingInputRepository,
            ValidationService validationService) : base(currentUser)
        {
            _executorsProvider = executorsProvider;
            _codeSnippetRepository = codeSnippetRepository;
            _wildcardsFactory = wildcardsFactory;
            _testingInputRepository = testingInputRepository;
            _validationService = validationService;
        }

        public List<LanguageIdentifier> GetSupportedLanguages()
        {
            return _executorsProvider.GetSupportedLanguages().ToList();
        }

        public CodeSnippetScaffoldingDto ScaffoldStartingLanguageSnippet(LanguageIdentifier language)
        {
            var codeGenerator = _executorsProvider.Get(language);
            var res = new CodeSnippetScaffoldingDto
            {
                CodeLanguage = language,
                Code = !string.IsNullOrEmpty(codeGenerator.LanguageConfiguration.StartingCodeSnippet)
                    ? codeGenerator.LanguageConfiguration.StartingCodeSnippet
                    : codeGenerator.LanguageConfiguration.SingleLineComment + "Write code here..."
            };
            return res;
        }


        public async Task<CodeSnippetScaffoldingDto> ScaffoldStartingSnippetForQuestionAnswer(int questionAnswerId,
            LanguageIdentifier languageIdentifier)
        {
            var dbCodeSnippet = await _codeSnippetRepository.GetSolutionSnippetForQuestionAnswer(questionAnswerId);

            var wildcardResult = _wildcardsFactory
                .SolutionCodeExtractorWildcard(languageIdentifier)
                .Apply(dbCodeSnippet.Code);

            return new CodeSnippetScaffoldingDto
            {
                Code = wildcardResult.TransformedInput,
                CodeLanguage = languageIdentifier
            };
        }

        private List<CodeExecutionResponseDto> BuildResponsesFromTaskResult(TaskResult taskResult)
        {
            if (taskResult.Status == CodeRunStatus.CompileError)
            {
                return new List<CodeExecutionResponseDto>
                {
                    new CodeExecutionResponseDto(null, taskResult.Message, null, CodeRunStatus.CompileError)
                };
            }

            return taskResult.ProcessRunResults
                .Select(r => r.ToCodeExecutionResponseDto())
                .ToList();
        }

        public async Task<List<CodeExecutionResponseDto>> RunCodeAsync(CodeExecutionRequestWithCustomInputDto request)
        {
            var taskResult = await RunCodeForTaskResultAsync(request);
            return BuildResponsesFromTaskResult(taskResult);
        }

        public async Task<TaskResult> RunCodeForTaskResultAsync(CodeExecutionRequestWithCustomInputDto request)
        {
            return await _executorsProvider.Get(request.Language).ExecuteCode(request);
        }

        public async Task<List<CodeExecutionResponseDto>> RunPublicTestingSetForQuestionAnswerAsync(
            int questionAnswerId, CodeExecutionRequestDto request)
        {
            TaskResult result = await RunQuestionTestingSetAsync(questionAnswerId, request);

            return BuildResponsesFromTaskResult(result);
        }

        public async Task<TaskResult> RunQuestionTestingSetAsync(int questionAnswerId, CodeExecutionRequestDto request)
        {
            var dbTestingInputs = await _testingInputRepository.GetByQuestionAnswerId(questionAnswerId);
            var requestWithInputs = new CodeExecutionRequestWithCustomInputDto
            {
                Code = request.Code,
                Language = request.Language,
                TestingInputs = dbTestingInputs.Select(x => x.ToTestingInputDto()).ToList()
            };

            var result = await RunCodeForTaskResultAsync(requestWithInputs);
            result = _validationService.ValidateResponsesWithTestingInputs(
                result,
                requestWithInputs.TestingInputs.ToImmutableDictionary(t => t.Id)
            );
            return result;
        }

        public async Task<CodeExecutionResponseDto> ApplyGeneratorAsync(InputGeneratorDto generator)
        {
            var testingInput = new TestingInputDto
            {
                Input = generator.CallArguments.Select(arg => arg.Value).JoinToString(Environment.NewLine)
            };
            var request = new CodeExecutionRequestWithCustomInputDto
            {
                Code = generator.CodeSnippet.Code,
                Language = generator.CodeSnippet.Language,
                TestingInputs = new List<TestingInputDto> {testingInput}
            };
            var result = await RunCodeForTaskResultAsync(request);
            
            return BuildResponsesFromTaskResult(result).First();
        }
    }
}