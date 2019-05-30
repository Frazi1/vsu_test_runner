using System;

namespace DataAccess.Model
{
    public interface ITimeTrackingEntity
    {
        DateTime CreatedAt { get; set; }
        DateTime? ModifiedAt { get; set; }
    }
}