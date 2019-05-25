using DataAccess.Model;

namespace DataAccess.Repository
{
    public class TestTemplateRepository : BaseRepository<DbTestTemplate>
    {
        public TestTemplateRepository(TestRunnerDbContext context) : base(context)
        {
        }
    }
}