using System.Collections.Generic;
using System.Linq;
using BusinessLayer.Executors;
using JetBrains.Annotations;
using SharedModels.DTOs;

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
    }
}