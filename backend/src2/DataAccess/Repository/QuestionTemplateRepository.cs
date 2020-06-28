using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Query;
using Utils;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class QuestionTemplateRepository : BaseEntityWithIdRepository<DbQuestionTemplate>
    {
        public QuestionTemplateRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public IQueryable<DbQuestionTemplate> QuestionTemplateWithSolutionAndInputsQuery(bool includeDeleted)
            => Set
                .Include(q => q.SolutionCodeSnippet)
                .Include(q => q.TestingInputs)
                .Where(q => includeDeleted || !q.IsDeleted);

        public IQueryable<DbQuestionTemplate> QuestionTemplateWithSectionsQuery()
            => QuestionTemplateWithSolutionAndInputsQuery(false)
                .Include(q => q.QuestionBankSection);

        public async Task<DbQuestionTemplate> GetWithSolutionByIdAsync(int id)
            => await QuestionTemplateWithSolutionAndInputsQuery(false).FirstAsync(t => t.Id == id);

        public async Task<List<DbQuestionTemplate>> GetWithSectionsAsync()
            => await QuestionTemplateWithSectionsQuery().ToListAsync();

        public async Task UpdateAndRemoveOld(DbQuestionTemplate updated)
        {
            Context.ChangeTracker.Entries().ForEach(e => e.State = EntityState.Detached);
            Set.Update(updated);
            var old = await GetWithSolutionByIdAsync(updated.Id);
            var toRemove = Context.ChangeTracker
                .Entries()
                .Where(e => e.State == EntityState.Unchanged)
                .Select(e => e.Entity);
            Context.RemoveRange(toRemove);
        }
    }
}