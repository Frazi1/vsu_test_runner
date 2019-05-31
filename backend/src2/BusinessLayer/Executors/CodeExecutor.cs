using System.Threading.Tasks;
using BusinessLayer.Executors.PipelineTasks;
using SharedModels.DTOs;

namespace BusinessLayer.Executors
{
    public class CodeExecutor
    {
        protected PipeLineTasksProvider PipelineTasksProvider { get; }
        protected PipeLine PipeLine { get; set; }

        public LanguageConfiguration LanguageConfiguration { get; }

        public CodeExecutor(LanguageConfiguration languageConfiguration,
            PipeLineTasksProvider pipePipelineTasksProvider)
        {
            PipelineTasksProvider = pipePipelineTasksProvider;
            LanguageConfiguration = languageConfiguration;
            PipeLine = new PipeLine()
                    .Add(PipelineTasksProvider.CreateOsWorkspaceTask())
                    .Add(PipelineTasksProvider.CreateSaveSourceCodeTask())
                    .Add(PipelineTasksProvider.CreateNoCompileCodeTask())
                    .Add(PipelineTasksProvider.CreateRunOsApplicationTask())
                ;
        }

        public async Task<TaskResult> ExecuteCode(CodeExecutionRequestDto request)
        {
            using (var pipelineState = new OsPipeLineState())
            {
                return await PipeLine.ExecuteTasks(pipelineState, request, LanguageConfiguration);
            }
        }
    }

    public class CompileCodeExecutor : CodeExecutor
    {
        public CompileCodeExecutor(
            LanguageConfiguration languageConfiguration,
            PipeLineTasksProvider pipePipelineTasksProvider)
            : base(languageConfiguration, pipePipelineTasksProvider)
        {
            PipeLine = new PipeLine()
                .Add(PipelineTasksProvider.CreateOsWorkspaceTask())
                .Add(PipelineTasksProvider.CreateSaveSourceCodeTask())
                .Add(PipelineTasksProvider.CreateCompileCodeTask())
                .Add(PipelineTasksProvider.CreateRunOsApplicationTask())
                ;
        }
    }
}