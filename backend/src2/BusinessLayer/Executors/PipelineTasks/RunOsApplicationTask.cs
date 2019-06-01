using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using DataAccess.Model;
using SharedModels.DTOs;
using SharedModels.Enum;
using Utils;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class RunOsApplicationTask : IPipeLineTask
    {
        private const int WaitTimeOut = 5000;

        public async Task Execute(IPipeLineState state, CodeExecutionRequestDto request,
            LanguageConfiguration config)
        {
            string executableFilePath = Path.Combine(state.WorkspaceId, state.ExecutableFileName);
            string runCmd = config.RunCmd.Replace("{outputFileName}", executableFilePath);
            string runCmdArgs = config.RunCmdArgs?.Replace("{outputFileName}", state.ExecutableFileName) ?? "";

            var processTuples = request.TestingInputs
                .Select(i =>
                {
                    var processStartInfo = new ProcessStartInfo
                    {
                        WorkingDirectory = state.WorkspaceId,
                        FileName = runCmd,
                        Arguments = runCmdArgs,
                        RedirectStandardError = true,
                        RedirectStandardInput = true,
                        RedirectStandardOutput = true,
                        UseShellExecute = false,
                    };
                    return (Input: i, ProcessStartInfo: processStartInfo);
                })
                .Select(t => (Input: t.Input, Task: Task.Run(async () =>
                {
                    var process = Process.Start(t.ProcessStartInfo);
                    if (process.StandardInput.BaseStream.CanWrite)
                    {
                        process.StandardInput.WriteLine(t.Input.Input);
                    }

                    process.WaitForExit(WaitTimeOut);
                    return process;
                })))
                .ToList();

            await Task.WhenAll(processTuples.Select(t => t.Task));

            var executionResults = processTuples
                .Select(t =>
                {
                    (TestingInputDto input, var task) = t;
                    if (task.Result.HasExited)
                        return new ProcessRunResult(
                            input.Id,
                            input.Input,
                            task.Result.StandardOutput.ReadToEnd().RemoveFromEndSafe(Environment.NewLine.Length),
                            task.Result.StandardError.ReadToEnd(),
                            CodeRunStatus.Success);
                    return new ProcessRunResult(input.Id, input.Input, "Timeout exceeded", null,
                        CodeRunStatus.TimeOutExceeded);
                }).ToList();

            state.ExecutionResults.AddRange(executionResults);
        }
    }
}