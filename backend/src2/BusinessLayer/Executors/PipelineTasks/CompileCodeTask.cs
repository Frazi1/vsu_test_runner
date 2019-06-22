using System.Diagnostics;
using System.IO;
using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using BusinessLayer.Executors.PipelineTasks.Exceptions;
using SharedModels.DTOs;
using Utils;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class CompileCodeTask : IConditionalPipeLineTask
    {
        public async Task Execute(IPipeLineState state, CodeExecutionRequestWithCustomInputDto request,
            LanguageConfiguration config)
        {
            string compileCmd = config.CompileCmd;
            string compileCmdTemplate = config.CompileCmdArgs;

            string compiledFileName = $"main.{config.ExecutableFileExt}";

            string compileCmdArgs = compileCmdTemplate
                .Replace("{inputFileName}", state.SourceFileName)
                .Replace("{outputFileName}", compiledFileName);

            var processStartInfo = new ProcessStartInfo
            {
                WorkingDirectory = state.WorkspaceId,
                FileName = compileCmd,
                Arguments = compileCmdArgs,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            };
            var process = Process.Start(processStartInfo);
            await Task.Run(() => process.WaitForExit());
            state.ExecutableFileName = compiledFileName;

            string output = await process.StandardOutput.ReadToEndAsync();
            string error = await process.StandardError.ReadToEndAsync();
            if (config.CheckCompiledFiles && !File.Exists(state.GetExecutableFilePath()))
            {
                throw new CompilationException(error.OrIfNullOrEmpty(output));
            }

            if (!string.IsNullOrEmpty(error))
            {
                throw new CompilationException(error);
            }
        }

        public bool ShouldExecute(IPipeLineState state, CodeExecutionRequestWithCustomInputDto request,
            LanguageConfiguration config)
        {
            return config.CompilationRequired;
        }
    }
}