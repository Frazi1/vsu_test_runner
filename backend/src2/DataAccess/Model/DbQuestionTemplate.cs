using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbQuestionTemplate: IEntityWithId
    {
        public DbQuestionTemplate()
        {
            TestingInputs = new HashSet<DbTestingInput>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int SolutionCodeSnippetId { get; set; }

        public virtual DbCodeSnippet SolutionCodeSnippet { get; set; }
        public virtual ICollection<DbTestingInput> TestingInputs { get; set; }
    }
}