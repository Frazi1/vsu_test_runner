using DataAccess.Model;
using JetBrains.Annotations;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class QuestionBankSectionRepository : BaseRepository<DbQuestionBankSection>
    {
        public QuestionBankSectionRepository(TestRunnerDbContext context)
            : base(context)
        {
        }

    }
}