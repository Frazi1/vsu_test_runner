using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using DataAccess.Repository.Interfaces;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class CodeSnippetRepository : BaseEntityWithIdRepository<DbCodeSnippet>
    {
        public CodeSnippetRepository(TestRunnerDbContext context)
            : base(context)
        {
        }

        public async Task<DbCodeSnippet> GetSolutionSnippetForQuestionAnswer(int questionAnswerId)
        {
            return await ((IRepository) this).Set<DbQuestionAnswer>()
                .Where(a => a.Id == questionAnswerId)
                .Select(a => a.QuestionInstance)
                .Select(i => i.QuestionTemplate)
                .Select(t => t.SolutionCodeSnippet).FirstAsync();
        }
    }
}