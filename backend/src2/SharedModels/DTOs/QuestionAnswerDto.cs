using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class QuestionAnswerDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public bool? ValidationPassed { get; set; }
        public bool IsValidated { get; set; }
        public List<CodeExecutionResponseDto> Iterations { get; set; }
        public CodeSnippetDto AnswerCodeSnippet { get; set; }
    }
}