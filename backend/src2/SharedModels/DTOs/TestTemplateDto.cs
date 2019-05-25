using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class TestTemplateDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int TimeLimit { get; set; }

        public virtual List<QuestionTemplateDto> QuestionTemplates { get; set; }
    }
}