using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Query;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class TestRunRepository: BaseRepository<DbTestRun>
    {
        public TestRunRepository(TestRunnerDbContext context) : base(context)
        {
        }

        private IQueryable<DbTestRun> GetFullQuery()
        {
            return Set
                .Include(r => r.QuestionAnswers)
                    .ThenInclude(a => a.CodeSnippet)
                .Include(r => r.QuestionAnswers)
                    .ThenInclude(a => a.QuestionInstance)
                .Include(r => r.QuestionAnswers)
                    .ThenInclude(r => r.CodeRunIterations)
                        .ThenInclude(i => i.TestingInput)
                .Include(r => r.TestInstance)
                    .ThenInclude(i => i.TestTemplate)
                        .ThenInclude(t => t.QuestionTemplates);
        }
        
        public async Task<List<DbTestRun>> GetAllFullAsync()
        {
            return await GetFullQuery().ToListAsync();
        }

        public async Task<DbTestRun> GetFullByIdAsync(int id)
        {
            return await GetFullQuery().FirstAsync(r => r.Id == id);
        }

    }
}