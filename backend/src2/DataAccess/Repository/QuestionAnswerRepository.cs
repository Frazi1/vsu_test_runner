using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class QuestionAnswerRepository: BaseRepository<DbQuestionAnswer>
    {
        public QuestionAnswerRepository(TestRunnerDbContext context) : base(context)
        {
        }

        public async Task<DbQuestionAnswer> GetWithSolutionCodeSnippetByIdAsync(int id)
        {
            return await Set.Include(a => a.CodeSnippet).FirstAsync(a => a.Id == id);
        }
    }
}