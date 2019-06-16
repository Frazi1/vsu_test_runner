using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class TestTemplatePermissionsController : BaseApiController
    {
        private readonly PermissionsService _permissionsService;

        public TestTemplatePermissionsController(PermissionsService permissionsService)
        {
            _permissionsService = permissionsService;
        }

        [HttpGet("{templateId}")]
        public async Task<List<TestTemplateUserPermissionsDto>> Get(int templateId)
        {
            return await _permissionsService.GetPermissionsForTestTemplateAsync(templateId);
        }

        [HttpPut("{templateId}")]
        public async Task Update(int templateId, [FromBody] List<TestTemplateUserPermissionsDto> permissions)
        {
            await _permissionsService.UpdatePermissionsForTestTemplateAsync(templateId, permissions);
        }
    }
}