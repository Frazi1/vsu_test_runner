using System.IO;
using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using SharedModels.DTOs;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class SaveSourceCodeTask : IPipeLineTask
    {
        public async Task Execute(IPipeLineState state, CodeExecutionRequestDto request,
            LanguageConfiguration config)
        {
            string fileExt = config.SourceFileExt;
            string sourceFileName = $"main.{fileExt}";
            string sourceFilePath = Path.Combine(state.WorkspaceId, sourceFileName);

            await File.WriteAllTextAsync(sourceFilePath, request.Code);
            state.SourceFileName = sourceFileName; 
        }
    }
}