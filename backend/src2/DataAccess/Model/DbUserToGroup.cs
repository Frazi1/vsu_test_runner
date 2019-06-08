namespace DataAccess.Model
{
    public class DbUserToGroup
    {
        public int UserId { get; set; }
        public int GroupId { get; set; }

        public virtual DbUser User { get; set; }
        public virtual DbGroup Group { get; set; }
    }
}