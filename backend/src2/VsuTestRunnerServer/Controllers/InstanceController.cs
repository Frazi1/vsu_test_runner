using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class InstanceController : BaseApiController
    {
        private readonly TestInstanceService _testInstanceService;

        public InstanceController(TestInstanceService testInstanceService)
        {
            _testInstanceService = testInstanceService;
        }
        
        [HttpGet]
        public async Task<List<TestInstanceDto>> GetAllTestInstancesAsync()
        {
            return await _testInstanceService.GetAllAsync();
        }

        [HttpGet("{id}")]
        public async Task<TestInstanceDto> GetTestInstanceByIdAsync(int id)
        {
            return await _testInstanceService.GetTestInstanceByIdAsync(id);
        }

        [HttpPost("create/{id}")]
        public async Task<int> CreateTestInstanceAsync(int id)
        {
            return await _testInstanceService.CreateTestInstanceByIdAsync(id);
        }
    }
}