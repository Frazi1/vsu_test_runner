using System;

namespace DataAccess.Model
{
    public class DbInputGenerator : IEntityWithId, ITimeTrackingEntity
    {
        public int Id { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? ModifiedAt { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public string CallParameters { get; set; }

        public int CodeSnippetId { get; set; }
        public int CreatedByUserId { get; set; }
        
        public virtual DbCodeSnippet CodeSnippet { get; set; }
        public virtual DbUser CreatedByUser { get; set; }
    }
}