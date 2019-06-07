using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class GeneratorController: BaseApiController
    {
        private readonly InputGeneratorService _inputGeneratorService;

        public GeneratorController(InputGeneratorService inputGeneratorService)
        {
            _inputGeneratorService = inputGeneratorService;
        }

        [HttpGet("{id}")]
        public async Task<InputGeneratorDto> GetById(int id)
        {
            return await _inputGeneratorService.GetFullByIdAsync(id);
        }
        
        [HttpGet]
        public async Task<List<InputGeneratorDto>> GetAll()
        {
            return await _inputGeneratorService.GetAllAsync();
        }

        [HttpPost]
        public async Task<int> Add([FromBody] InputGeneratorDto generator)
        {
            return (await _inputGeneratorService.AddAsync(generator)).Id;
        }

        [HttpPut("{id}")]
        public async Task Update(int id, [FromBody] InputGeneratorDto generator)
        {
            await _inputGeneratorService.UpdateAsync(generator);
        }
    }
}