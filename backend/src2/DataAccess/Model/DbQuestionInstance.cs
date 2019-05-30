using System;
using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbQuestionInstance : IEntityWithId, ITimeTrackingEntity
    {
        public DbQuestionInstance()
        {
            QuestionAnswers = new List<DbQuestionAnswer>();
        }

        public int Id { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? ModifiedAt { get; set; }

        public int TestInstanceId { get; set; }
        public int QuestionTemplateId { get; set; }
        
        public virtual DbTestInstance TestInstance { get; set; }
        public virtual DbQuestionTemplate QuestionTemplate { get; set; }

        public ICollection<DbQuestionAnswer> QuestionAnswers { get; set; }
    }
}