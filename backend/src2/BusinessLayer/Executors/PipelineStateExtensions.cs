using System.IO;
using BusinessLayer.Executors.Interfaces;

namespace BusinessLayer.Executors
{
    public static class PipelineStateExtensions
    {
        public static string GetSourceFilePath(this IPipeLineState state)
            => Path.Combine(state.WorkspaceId, state.SourceFileName);

        public static string GetExecutableFilePath(this IPipeLineState state)
            => Path.Combine(state.WorkspaceId, state.ExecutableFileName);
    }
}