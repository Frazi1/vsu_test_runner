using DataAccess.Model;
using JetBrains.Annotations;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class QuestionAnswerRepository: BaseEntityWithIdRepository<DbQuestionAnswer>
    {
        public QuestionAnswerRepository(TestRunnerDbContext context) : base(context)
        {
        }
    }
}