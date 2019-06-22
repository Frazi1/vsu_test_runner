using System.Collections.Generic;
using JetBrains.Annotations;

namespace SharedModels.DTOs
{
    public class QuestionBankSectionDto
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public int? ParentSectionId { get; set; }

        public ICollection<QuestionTemplateDto> QuestionTemplates { get; set; }

        [UsedImplicitly]
        public QuestionBankSectionDto()
        {
        }

        public QuestionBankSectionDto(int id, string name, int? parentSectionId, ICollection<QuestionTemplateDto> questionTemplates)
        {
            Id = id;
            Name = name;
            ParentSectionId = parentSectionId;
            QuestionTemplates = questionTemplates;
        }
    }
}