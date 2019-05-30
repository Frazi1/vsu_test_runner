using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class TestInstanceRepository : BaseRepository<DbTestInstance>
    {
        public TestInstanceRepository(TestRunnerDbContext context) : base(context)
        {
        }

        private IQueryable<DbTestInstance> SetWithTemplates()
        {
            return Set
                .Include(d => d.TestTemplate)
                .Include(d => d.QuestionInstances).ThenInclude(q => q.QuestionTemplate);
        }

        public async Task<List<DbTestInstance>> GetTestsInstancesWithTemplates()
        {
            return await SetWithTemplates().ToListAsync();
        }

        public async Task<DbTestInstance> GetTestsInstanceWithTemplateByIdAsync(int id)
        {
            return await SetWithTemplates().FirstAsync(d => d.Id == id);
        }
    }
}