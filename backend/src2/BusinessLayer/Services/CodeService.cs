using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Runtime.Serialization;
using System.Threading.Tasks;
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
            ExecutorsProvider executorsProvider,
            CodeSnippetRepository codeSnippetRepository,
            WildcardsFactory wildcardsFactory,
            TestingInputRepository testingInputRepository,
            ValidationService validationService)
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
                .Select(r => new CodeExecutionResponseDto(r.Input, r.Output.OrIfNullOrEmpty(r.Error), r.IsValid, r.Status))
                .ToList();
        }

        public async Task<List<CodeExecutionResponseDto>> RunCodeAsync(CodeExecutionRequestDto request)
        {
            var taskResult = await RunCodeForTaskResultAsync(request);
            return BuildResponsesFromTaskResult(taskResult);
        }

        public async Task<TaskResult> RunCodeForTaskResultAsync(CodeExecutionRequestDto request)
        {
            return await _executorsProvider.Get(request.Language).ExecuteCode(request);
        }

        public async Task<List<CodeExecutionResponseDto>> RunPublicTestingSetForQuestionAnswerAsync(
            int questionAnswerId, CodeExecutionRequestDto request)
        {
            var dbTestingInputs = await _testingInputRepository.GetByQuestionAnswerId(questionAnswerId);
            request.TestingInputs = dbTestingInputs.Select(x => x.ToTestingInputDto()).ToList();

            var result = await RunCodeForTaskResultAsync(request);
            _validationService.ValidateResponsesWithTestingInputs(
                result.ProcessRunResults,
                request.TestingInputs.ToImmutableDictionary(t => t.Id)
            );
            
            return BuildResponsesFromTaskResult(result);
        }
    }
}