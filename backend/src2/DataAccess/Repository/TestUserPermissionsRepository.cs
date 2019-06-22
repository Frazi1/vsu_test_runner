using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class TestUserPermissionsRepository : BaseEntityWithIdRepository<DbTestTemplateUserPermission>
    {
        public TestUserPermissionsRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public async Task<List<DbTestTemplateUserPermission>> GetByTestTemplateIdAsync(int testTemplateId)
        {
            return await Set
                .Include(p => p.User)
                .Where(p => p.TestTemplateId == testTemplateId)
                .ToListAsync();
        }
    }
}