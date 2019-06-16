using SharedModels.DTOs;

namespace BusinessLayer.Executors.Interfaces
{
    public interface IConditionalPipeLineTask: IPipeLineTask
    {
        bool ShouldExecute(IPipeLineState state, CodeExecutionRequestWithCustomInputDto request,
            LanguageConfiguration config);
        
    }
}