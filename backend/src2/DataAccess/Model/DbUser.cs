using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbUser: IEntityWithId
    {
        public int Id { get; set; }
        public string Email { get; set; }
        public string UserName { get; set; }
        public string PasswordHash { get; set; }

        public ICollection<DbUserToGroup> Groups { get; set; }
    }
}