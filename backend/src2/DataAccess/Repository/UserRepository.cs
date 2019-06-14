using DataAccess.Model;
using JetBrains.Annotations;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class UserRepository: BaseRepository<DbUser>
    {
        public UserRepository(TestRunnerDbContext context) : base(context)
        {
        }
    }
}