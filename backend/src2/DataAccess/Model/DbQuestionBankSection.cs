using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbQuestionBankSection
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public int ParentSectionId { get; set; }
        public DbQuestionBankSection ParentSection { get; set; }

        public ICollection<DbQuestionTemplate> QuestionTemplates { get; set; }
    }
}