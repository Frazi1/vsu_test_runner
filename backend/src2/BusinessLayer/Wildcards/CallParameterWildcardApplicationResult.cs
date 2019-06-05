using System.Collections.Immutable;
using SharedModels.DTOs;

namespace BusinessLayer.Wildcards
{
    public class CallParameterWildcardApplicationResult : WildcardApplicationResult
    {
        public ImmutableList<GeneratorCallArgumentDto> CallArguments { get; }

        public CallParameterWildcardApplicationResult(
            string transformedInput,
            ImmutableList<GeneratorCallArgumentDto> callArguments)
            : base(transformedInput)
        {
            CallArguments = callArguments;
        }
    }
}