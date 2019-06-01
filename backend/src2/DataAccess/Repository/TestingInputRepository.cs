using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class TestingInputRepository: BaseRepository<DbTestingInput>
    {
        public TestingInputRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public async Task<List<DbTestingInput>> GetByQuestionAnswerId(int questionAnswerId)
        {
            return await Context.QuestionAnswers
                .Where(a => a.Id == questionAnswerId)
                .Select(a => a.QuestionInstance)
                .Select(i => i.QuestionTemplate)
                .SelectMany(t => t.TestingInputs)
                .ToListAsync();
        }
    }
}