using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class QuestionTemplateDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }

        public virtual CodeSnippetDto SolutionCodeSnippet { get; set; }
        public virtual List<TestingInputDto> TestingInputs { get; set; }
    }
}