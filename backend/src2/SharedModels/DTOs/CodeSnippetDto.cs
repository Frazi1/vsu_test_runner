using SharedModels.Enum;

namespace SharedModels.DTOs{
    public class CodeSnippetDto
    {
        public int Id { get; set; }
        public string Code { get; set; }
        public CodeLanguage Language { get; set; }
    }
}