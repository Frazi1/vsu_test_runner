using System.Collections.Generic;
using System.IO;
using BusinessLayer.Executors.Interfaces;
using BusinessLayer.Executors.PipelineTasks;
using DataAccess.Model;
using SharedModels.Enum;

namespace BusinessLayer.Executors
{
    public class OsPipeLineState : IPipeLineState
    {
        public string WorkspaceId { get; set; }
        public string SourceFileName { get; set; }
        public string ExecutableFileName { get; set; }
        public List<ProcessRunResult> ExecutionResults { get; set; } = new List<ProcessRunResult>();
        public CodeRunStatus? Status { get; set; }
        
        public void Dispose()
        {
            Directory.Delete(WorkspaceId, true);
        }
    }
}