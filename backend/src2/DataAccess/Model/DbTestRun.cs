using System;
using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbTestRun : IEntityWithId, ITimeTrackingEntity
    {
        public DbTestRun()
        {
            QuestionAnswers = new List<DbQuestionAnswer>();
        }

        public int Id { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? ModifiedAt { get; set; }
        public DateTime? FinishedAt { get; set; }

        //TODO: not nullable
        public int? UserId { get; set; }
        public int TestInstanceId { get; set; }
        
        public virtual DbUser User { get; set; }
        public virtual ICollection<DbQuestionAnswer> QuestionAnswers { get; set; }
        public virtual DbTestInstance TestInstance { get; set; }
    }
}