using System.Collections.Generic;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class GroupRepository : BaseEntityWithIdRepository<DbGroup>
    {
        public GroupRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public async Task<List<DbGroup>> GetAllWithUsersAsync()
            => await Set.Include(g => g.Users).ThenInclude(a => a.User).ToListAsync();
    }
}