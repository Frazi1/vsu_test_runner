using System.Collections.Immutable;
using SharedModels.DTOs;

namespace BusinessLayer.Executors
{
    public class ExecutorsProvider
    {
        private readonly IImmutableDictionary<LanguageIdentifier, CodeExecutor> _executors;

        public ExecutorsProvider(IImmutableDictionary<LanguageIdentifier, CodeExecutor> executors)
        {
            _executors = executors;
        }

        public CodeExecutor Get(LanguageIdentifier language) => _executors[language];

        public ImmutableList<LanguageIdentifier> GetSupportedLanguages() => _executors.Keys.ToImmutableList();
    }
}