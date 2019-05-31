using System.Collections.Immutable;
using SharedModels.DTOs;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class PipeLineTasksProvider
    {
        private readonly string _baseWorkDirPath;

        public PipeLineTasksProvider(string baseWorkDirPath)
        {
            _baseWorkDirPath = baseWorkDirPath;
        }

        public CompileCodeTask CreateCompileCodeTask() => new CompileCodeTask();
        public NoCompileCodeTask CreateNoCompileCodeTask() => new NoCompileCodeTask();
        public CreateOsWorkspaceTask CreateOsWorkspaceTask() => new CreateOsWorkspaceTask(_baseWorkDirPath);
        public SaveSourceCodeTask CreateSaveSourceCodeTask() => new SaveSourceCodeTask();
        public RunOsApplicationTask CreateRunOsApplicationTask() => new RunOsApplicationTask();
    }
}