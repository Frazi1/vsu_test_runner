using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Threading.Tasks;
using BusinessLayer.Executors;
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

        public CodeService(
            ExecutorsProvider executorsProvider,
            CodeSnippetRepository codeSnippetRepository,
            WildcardsFactory wildcardsFactory)
        {
            _executorsProvider = executorsProvider;
            _codeSnippetRepository = codeSnippetRepository;
            _wildcardsFactory = wildcardsFactory;
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

        public async Task<List<CodeExecutionResponseDto>> RunCode(CodeExecutionRequestDto request)
        {
            var taskResult = await _executorsProvider.Get(request.Language).ExecuteCode(request);
            if (taskResult.Status == CodeRunStatus.CompileError)
            {
                return new List<CodeExecutionResponseDto>
                {
                    new CodeExecutionResponseDto(null, taskResult.Message, null, CodeRunStatus.CompileError)
                };
            }

            return taskResult.ProcessRunResults
                .Select(r => new CodeExecutionResponseDto(r.Input, r.Output.OrIfNullOrEmpty(r.Error), null, r.Status))
                .ToList();
        }
    }
}