using System.Collections.Generic;
using DataAccess.Model;
using SharedModels.Enum;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class TaskResult
    {
        public CodeRunStatus Status { get; }
        public string Message { get; }
        public List<ProcessRunResult> ProcessRunResults { get; }

        public TaskResult(CodeRunStatus status, string message)
        {
            Status = status;
            Message = message;
            ProcessRunResults = new List<ProcessRunResult>();
        }

        public static TaskResult Success => new TaskResult(CodeRunStatus.Success, string.Empty);
    }
}