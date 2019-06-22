using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbQuestionTemplate: IEntityWithId
    {
        public DbQuestionTemplate()
        {
            TestingInputs = new HashSet<DbTestingInput>();
            TestTemplates = new List<DbTestTemplateToQuestion>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int SolutionCodeSnippetId { get; set; }
        public bool IsOpen { get; set; } = false;

        public int? QuestionBankSectionId { get; set; }
        public DbQuestionBankSection QuestionBankSection { get; set; }

        public virtual DbCodeSnippet SolutionCodeSnippet { get; set; }
        public virtual ICollection<DbQuestionInstance> QuestionInstances { get; set; }
        public virtual ICollection<DbTestingInput> TestingInputs { get; set; }
        public virtual ICollection<DbTestTemplateToQuestion> TestTemplates { get; set; }
    }
}