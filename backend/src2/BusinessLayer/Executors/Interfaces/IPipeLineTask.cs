using System.Threading.Tasks;
using BusinessLayer.Executors.PipelineTasks;
using SharedModels.DTOs;

namespace BusinessLayer.Executors.Interfaces
{
    public interface IPipeLineTask
    {
        Task Execute(IPipeLineState state, CodeExecutionRequestWithCustomInputDto request, LanguageConfiguration config);
    }
}