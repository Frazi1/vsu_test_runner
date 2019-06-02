using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    [Route("api/finished_run")]
    public class FinishedRunController : BaseApiController
    {
        private readonly TestRunService _testRunService;

        public FinishedRunController(TestRunService testRunService)
        {
            _testRunService = testRunService;
        }

        [HttpGet("{id}")]
        public async Task<TestRunDto> GetFinishedTestRunById(int id)
        {
            return await _testRunService.GetFinishedTestRunByIdAsync(id);
        }
    }
}