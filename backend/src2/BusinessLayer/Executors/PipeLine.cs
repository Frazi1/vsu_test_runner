using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using BusinessLayer.Executors.PipelineTasks;
using BusinessLayer.Executors.PipelineTasks.Exceptions;
using DataAccess.Model;
using SharedModels.DTOs;
using SharedModels.Enum;

namespace BusinessLayer.Executors
{
    public class PipeLine
    {
        public List<IPipeLineTask> Tasks { get; set; }

        public PipeLine()
        {
            Tasks = new List<IPipeLineTask>();
        }

        public PipeLine Add(IPipeLineTask task)
        {
            Tasks.Add(task);
            return this;
        }

        public async Task<TaskResult> ExecuteTasks(IPipeLineState state, CodeExecutionRequestWithCustomInputDto request,
            LanguageConfiguration languageConfiguration)
        {
            foreach (var task in Tasks)
            {
                try
                {
                    await task.Execute(state, request, languageConfiguration);
                }
                catch (CompilationException e)
                {
                    return new TaskResult(CodeRunStatus.CompileError, e.Message);
                }
            }

            var result = TaskResult.Success;
            result.ProcessRunResults.AddRange(state.ExecutionResults);
            return result;
        }
    }
}