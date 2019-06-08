using System.Threading.Tasks;
using DataAccess;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace VsuTestRunnerServer.Controllers
{
    [AllowAnonymous]
    public class DbController : BaseApiController
    {
        [HttpGet]
        public string Hello()
        {
            return "Hello world";
        }

        [HttpGet("recreate")]
        public async Task<string> RecreateDb([FromServices] TestRunnerDbContext context)
        {
            await context.Database.EnsureDeletedAsync();
            await context.Database.EnsureCreatedAsync();
            return "Success";
        }
    }
}