using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using DataAccess.Model;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class TemplateController : BaseApiController
    {
        private readonly TemplateService _service;

        public TemplateController(TemplateService service)
        {
            _service = service;
        }

        // GET: api/Template1
        [HttpGet]
        public async Task<List<TestTemplateDto>> GetAllTemplates([FromQuery] bool includeDeleted = false)
        {
            return await _service.GetAllTemplatesAsync();
        }

        // GET: api/Template1/5
        [HttpGet("{id}", Name = "Get")]
        public async Task<TestTemplateDto> GetTemplateById(int id)
        {
            return await _service.GetTemplateByIdAsync(id);
        }

        // POST: api/Template1
        [HttpPost]
        public async Task<int> Post([FromBody] TestTemplateDto template)
        {
            return (await _service.AddTestTemplateAsync(template)).Id;
        }

        // PUT: api/Template1/5
        [HttpPut("{id}")]
        public async Task Put(int id, [FromBody] TestTemplateDto templateDto)
        {
            await _service.UpdateTestTemplateAsync(templateDto);
        }

        // DELETE: api/ApiWithActions/5
        [HttpDelete("{id}")]
        public async Task Delete(int id)
        {
            await _service.DeleteTemplateByIdAsync(id);
        }
    }
}