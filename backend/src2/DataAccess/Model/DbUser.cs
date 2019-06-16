using System.Collections.Generic;
using SharedModels.Enum;

namespace DataAccess.Model
{
    public class DbUser : IEntityWithId
    {
        public DbUser()
        {
            Groups = new List<DbUserToGroup>();
            Features = new HashSet<DbUserFeature>();
        }
        
        public int Id { get; set; }
        public string Email { get; set; }
        public string UserName { get; set; }
        public string PasswordHash { get; set; }
        public string FirstName { get; set; }
        public string MiddleName { get; set; }
        public string LastName { get; set; }

        public UserType Type { get; set; }
        public ICollection<DbUserToGroup> Groups { get; set; }
        public ICollection<DbUserFeature> Features { get; set; }
    }
}