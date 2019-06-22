using System.Collections.Generic;
using JetBrains.Annotations;

namespace SharedModels.DTOs
{
    public class QuestionTemplateDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public bool IsOpen { get; set; }
        public int? QuestionBankSectionId { get; set; }

        public virtual CodeSnippetDto CodeSnippet { get; set; }
        public virtual List<TestingInputDto> TestingInputs { get; set; }

        [UsedImplicitly]
        public QuestionTemplateDto()
        {
        }

        public QuestionTemplateDto(int id, string name, string description, bool isOpen, int? questionBankSectionId,
            CodeSnippetDto codeSnippet, List<TestingInputDto> testingInputs)
        {
            Id = id;
            Name = name;
            Description = description;
            IsOpen = isOpen;
            QuestionBankSectionId = questionBankSectionId;
            CodeSnippet = codeSnippet;
            TestingInputs = testingInputs;
        }
    }
}