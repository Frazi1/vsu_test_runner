using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using SharedModels.DTOs;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class NoCompileCodeTask: IPipeLineTask
    {
        public Task Execute(IPipeLineState state, CodeExecutionRequestDto request,
            LanguageConfiguration config)
        {
            state.ExecutableFileName = state.SourceFileName;
            return Task.CompletedTask;
        }
    }
}