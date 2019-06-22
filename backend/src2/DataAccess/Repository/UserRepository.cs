using DataAccess.Model;
using JetBrains.Annotations;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class UserRepository: BaseEntityWithIdRepository<DbUser>
    {
        public UserRepository(TestRunnerDbContext context) : base(context)
        {
        }
    }
}