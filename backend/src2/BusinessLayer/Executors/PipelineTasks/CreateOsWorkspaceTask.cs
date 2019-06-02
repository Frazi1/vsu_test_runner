using System;
using System.IO;
using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using SharedModels.DTOs;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class CreateOsWorkspaceTask : IPipeLineTask
    {
        private readonly string _basePath;

        public CreateOsWorkspaceTask(string basePath)
        {
            _basePath = basePath;
        }
        
        public Task Execute(IPipeLineState state, CodeExecutionRequestWithCustomInputDto request,
            LanguageConfiguration config)
        {
            string dirName = Guid.NewGuid().ToString();
            string dirPath = Path.Combine(_basePath, dirName);
            Directory.CreateDirectory(dirPath);

            state.WorkspaceId = dirPath;
            
            return Task.CompletedTask;
        }
    }
}