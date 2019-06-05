using System.Collections.Immutable;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer.Wildcards
{
    [UsedImplicitly]
    public class WildcardsFactory
    {
        private readonly IImmutableDictionary<LanguageIdentifier, LanguageConfiguration> _languageConfigurations;

        public WildcardsFactory(IImmutableDictionary<LanguageIdentifier, LanguageConfiguration> languageConfigurations)
        {
            _languageConfigurations = languageConfigurations;
        }

        public SolutionCodeExtractorWildcard SolutionCodeExtractorWildcard(LanguageIdentifier language)
            => new SolutionCodeExtractorWildcard(_languageConfigurations[language].SingleLineComment,
                "Write code here..");
        
        public CallParameterWildcard CallParameterWildcard(LanguageIdentifier language)
            => new CallParameterWildcard(_languageConfigurations[language].SingleLineComment);
    }
}