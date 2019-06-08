using DataAccess.Model;
using JetBrains.Annotations;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class GroupRepository : BaseRepository<DbGroup>
    {
        public GroupRepository(TestRunnerDbContext context) : base(context)
        {
        }
    }
}