namespace DataAccess.Model
{
    public abstract class DbTestInstanceAssignee: IEntityWithId
    {
        public int Id { get; set; }
        public InstanceAssigneeType AssigneeType { get; set; }
        
        public int TestInstanceId { get; set; }
        public DbTestInstance TestInstance { get; set; }
    }

    public enum InstanceAssigneeType
    {
        User = 1,
        Group = 2
    }

    public class DbTestInstanceGroupAssignee : DbTestInstanceAssignee
    {
        public int GroupId { get; set; }
        public virtual DbGroup Group { get; set; }
    }

    public class DbTestInstanceUserAssignee : DbTestInstanceAssignee
    {
        public int UserId { get; set; }
        public virtual DbUser User { get; set; }
    }
}