using System;
using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbTestInstance : IEntityWithId, ITimeTrackingEntity
    {
        public DbTestInstance()
        {
            QuestionInstances = new List<DbQuestionInstance>();
            IsActive = true;
        }

        public int Id { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? ModifiedAt { get; set; }
        public DateTime? AvailableAfter { get; set; }
        public DateTime? DisabledAfter { get; set; }
        public bool IsActive { get; set; }
        
        public int TestTemplateId { get; set; }
        
        public virtual DbTestTemplate TestTemplate { get; set; }
        public virtual ICollection<DbQuestionInstance> QuestionInstances { get; set; }
        public virtual ICollection<DbTestInstanceUserAssignee> AssignedUsers { get; set; }
        public virtual ICollection<DbTestInstanceGroupAssignee> AssignedGroups { get; set; }
        
    }
}