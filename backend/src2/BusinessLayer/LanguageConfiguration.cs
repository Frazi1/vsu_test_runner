using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer
{
    [UsedImplicitly]
    public class LanguageConfiguration
    {
        public string Id { get; set; }
        public string DisplayName { get; set; }
        public string RunCmd { get; set; }
        public string RunCmdArgs { get; set; }
        public string SingleLineComment { get; set; }
        public string CompileCmd { get; set; }
        public string CompileCmdArgs { get; set; }
        public string StartingCodeSnippet { get; set; }
        public string SourceFileExt { get; set; }
        public string ExecutableFileExt { get; set; }

        public LanguageIdentifier LanguageIdentifier => LanguageIdentifier.FromString(Id);
        public bool CompilationRequired => !string.IsNullOrEmpty(CompileCmd);
    }
}