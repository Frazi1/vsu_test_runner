
namespace SharedModels.DTOs{
    public class CodeSnippetDto
    {
        public int Id { get; set; }
        public string Code { get; set; }
        public LanguageIdentifier Language { get; set; }
    }
}