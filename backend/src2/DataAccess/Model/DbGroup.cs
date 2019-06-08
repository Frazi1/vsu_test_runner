using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbGroup: IEntityWithId
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        
        public int? ParentGroupId { get; set; }

        public DbGroup ParentGroup { get; set; }
        public virtual ICollection<DbUserToGroup> Users { get; set; }
    }
}