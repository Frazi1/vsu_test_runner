using System;
using System.Collections.Generic;
using BusinessLayer.Executors.PipelineTasks;
using SharedModels.Enum;

namespace BusinessLayer.Executors.Interfaces
{
    public interface IPipeLineState: IDisposable
    {
        string WorkspaceId { get; set; }
        string SourceFileName { get; set; }
        string ExecutableFileName { get; set; }
        List<ProcessRunResult> ExecutionResults { get; set; }
        CodeRunStatus? Status { get; set; }
    }
}