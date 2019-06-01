using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class CodeSnippetRepository : BaseRepository<DbCodeSnippet>
    {
        public CodeSnippetRepository(TestRunnerDbContext context)
            : base(context)
        {
        }

        public async Task<DbCodeSnippet> GetSolutionSnippetForQuestionAnswer(int questionAnswerId)
        {
            return await Context.QuestionAnswers
                .Where(a => a.Id == questionAnswerId)
                .Select(a => a.QuestionInstance)
                .Select(i => i.QuestionTemplate)
                .Select(t => t.SolutionCodeSnippet).FirstAsync();
        }
    }
}