using System;
using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbQuestionAnswer: IEntityWithId, ITimeTrackingEntity
    {
        public int Id { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? ModifiedAt { get; set; }

        public bool? ValidationPassed { get; set; }
        public DateTime? ValidatedAt { get; set; }
        
        public int QuestionInstanceId { get; set; }
        public int CodeSnippetId { get; set; }
        public int TestRunId { get; set; }
        
        public virtual DbQuestionInstance QuestionInstance { get; set; }
        public virtual DbCodeSnippet CodeSnippet { get; set; }
        public virtual DbTestRun TestRun { get; set; }
        public virtual ICollection<DbCodeRunIteration> CodeRunIterations { get; set; }
    }
}