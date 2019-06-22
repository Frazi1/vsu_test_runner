using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.ChangeTracking;
using Microsoft.EntityFrameworkCore.Query;
using Utils;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class TestTemplateRepository : BaseEntityWithIdRepository<DbTestTemplate>
    {
        public TestTemplateRepository(TestRunnerDbContext context) : base(context)
        {
        }

        private IIncludableQueryable<DbTestTemplate, DbCodeSnippet> GetFullQuery()
            => Context.TestTemplates
                .Include(t => t.QuestionTemplates)
                    .ThenInclude(t => t.QuestionTemplate)
                        .ThenInclude(t => t.TestingInputs)
                .Include(t => t.QuestionTemplates)
                    .ThenInclude(t => t.QuestionTemplate.SolutionCodeSnippet);


        public async Task<DbTestTemplate> GetFullByIdAsync(int id)
            => await GetFullQuery().FirstAsync(t => t.Id == id);

        public async Task<List<DbTestTemplate>> GetAllFullAsync()
            => await GetFullQuery().ToListAsync();

        public override async Task Update(DbTestTemplate updated)
        {
            Context.ChangeTracker.Entries().ForEach(e => e.State = EntityState.Detached);
            Set.Update(updated);
            var old = await GetFullByIdAsync(updated.Id);
            var toRemove = Context.ChangeTracker
                .Entries()
                .Where(e => e.State == EntityState.Unchanged)
                .Select(e => e.Entity);
            Context.RemoveRange(toRemove);
        }
    }
}