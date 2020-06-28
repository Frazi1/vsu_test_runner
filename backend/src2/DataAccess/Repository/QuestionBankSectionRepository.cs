using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class QuestionBankSectionRepository : BaseRepository<DbQuestionBankSection>
    {
        public QuestionBankSectionRepository(TestRunnerDbContext context)
            : base(context)
        {
        }

        public async Task<List<DbQuestionBankSection>> GetWithQuestionHeadersAsync(bool includeClosed, bool includeDeleted)
        {
            var res = await Set.Include(a => a.QuestionTemplates).Select(a => new
                {
                    a.Id,
                    a.Name,
                    a.ParentSection,
                    a.ParentSectionId,
                    QuestionTemplates = a.QuestionTemplates.Where(t => includeClosed || t.IsOpen).Where(t=> includeDeleted || !t.IsDeleted)
                })
                .ToListAsync();
            return res.Select(a => new DbQuestionBankSection
            {
                Id = a.Id,
                Name = a.Name,
                ParentSection = a.ParentSection,
                ParentSectionId = a.ParentSectionId,
                QuestionTemplates = a.QuestionTemplates.ToList()
            }).ToList();
        }
    }
}