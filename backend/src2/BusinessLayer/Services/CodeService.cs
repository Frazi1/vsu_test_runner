using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Threading.Tasks;
using BusinessLayer.Executors;
using DataAccess.Model;
using JetBrains.Annotations;
using SharedModels.DTOs;
using SharedModels.Enum;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class CodeService : BaseService
    {
        private readonly ExecutorsProvider _executorsProvider;

        public CodeService(ExecutorsProvider executorsProvider)
        {
            _executorsProvider = executorsProvider;
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
                .Select(r => new CodeExecutionResponseDto(r.Input, r.Output, null, r.Status))
                .ToList();
        }
    }
}