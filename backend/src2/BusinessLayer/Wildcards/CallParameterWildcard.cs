using System.Collections.Immutable;
using System.Linq;
using SharedModels.DTOs;

namespace BusinessLayer.Wildcards
{
    public class CallParameterWildcard : UnaryWildcard
    {
        public CallParameterWildcard(string languageComment)
            : base(languageComment, @"@CallArg:(?<ArgName>\w+)")
        {
        }

        public CallParameterWildcardApplicationResult GetCallParameters(string input)
        {
            var args = WildcardRegex.Matches(input)
                .Select(m => m.Groups["ArgName"].Value)
                .Select(name => new GeneratorCallArgumentDto {Name = name})
                .ToImmutableList();

            return new CallParameterWildcardApplicationResult(input, args);
        }

        public override WildcardApplicationResult Apply(string input)
        {
            return GetCallParameters(input);
        }
    }
}