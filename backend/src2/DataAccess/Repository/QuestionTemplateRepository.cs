using System.Collections.Generic;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Query;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class QuestionTemplateRepository : BaseEntityWithIdRepository<DbQuestionTemplate>
    {
        public QuestionTemplateRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public async Task<DbQuestionTemplate> GetWithSolutionByIdAsync(int id)
        {
            return await WithSolutionAndInputs().FirstAsync(t => t.Id == id);
        }
        
        public async Task<List<DbQuestionTemplate>> GetWithSectionsAsync()
        {
            return await WithSolutionAndInputs()
                .Include(q => q.QuestionBankSection)
                .ToListAsync();
        }

        private IIncludableQueryable<DbQuestionTemplate, ICollection<DbTestingInput>> WithSolutionAndInputs()
        {
            return Set.Include(q => q.SolutionCodeSnippet)
                .Include(q => q.TestingInputs);
        }
    }
}