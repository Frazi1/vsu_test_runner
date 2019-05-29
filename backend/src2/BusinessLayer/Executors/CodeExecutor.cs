namespace BusinessLayer.Executors
{
    public class CodeExecutor
    {
        public LanguageConfiguration LanguageConfiguration { get; }

        public CodeExecutor(LanguageConfiguration languageConfiguration)
        {
            LanguageConfiguration = languageConfiguration;
        }
    }

    public class CompileCodeExecutor : CodeExecutor
    {
        public CompileCodeExecutor(LanguageConfiguration languageConfiguration) : base(languageConfiguration)
        {
        }
    }
}