using System.Diagnostics;
using System.Threading.Tasks;
using BusinessLayer.Executors.Interfaces;
using SharedModels.DTOs;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class CompileCodeTask : IPipeLineTask
    {
        public async Task Execute(IPipeLineState state, CodeExecutionRequestDto request,
            LanguageConfiguration config)
        {
            string compileCmd = config.CompileCmd;
            string compileCmdTemplate = config.CompileCmdArgs;

            string compiledFileName = $"main.{config.ExecutableFileExt}";

            string compileCmdArgs = compileCmdTemplate
                .Replace("{inputFileName}", state.SourceFileName)
                .Replace("{outputFileName}", compiledFileName);
//            var strings = compileCmd.Split(new[] {" "}, StringSplitOptions.RemoveEmptyEntries);
//            string appName = strings[0];
//            var args = strings.Skip(1).JoinToString(" ");

            var processStartInfo = new ProcessStartInfo
            {
                WorkingDirectory = state.WorkspaceId,
                FileName = compileCmd,
                Arguments = compileCmdArgs
            };
            var process = Process.Start(processStartInfo);
            await Task.Run(() => process.WaitForExit());
            
            state.ExecutableFileName = compiledFileName;
        }
    }
}