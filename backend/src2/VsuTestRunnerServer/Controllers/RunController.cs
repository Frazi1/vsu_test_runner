using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class RunController : BaseApiController
    {
        private readonly TestRunService _testRunService;

        public RunController(TestRunService testRunService)
        {
            _testRunService = testRunService;
        }

        [HttpGet]
        public async Task<List<TestRunDto>> GetActiveTestRunsAsync()
        {
            return await _testRunService.GetActiveTestRunsAsync();
        }

        [HttpGet("{id}")]
        public async Task<TestRunDto> GetTestRunByIdAsync(int id)
        {
            return await _testRunService.GetActiveTestRunByIdAsync(id);
        }

        [HttpPost("{id}")]
        public async Task<int> StartTestRunFromTestInstanceAsync(int id)
        {
            return await _testRunService.StartTestRunFromTestInstanceAsync(id);
        }

        [HttpPut("{id}")]
        public async Task UpdateTestRunAnswersAsync(int id, [FromBody] List<QuestionAnswerUpdateDto> answerUpdates)
        {
            await _testRunService.UpdateTestRunAnswersAsync(id, answerUpdates);
        }
    }
}