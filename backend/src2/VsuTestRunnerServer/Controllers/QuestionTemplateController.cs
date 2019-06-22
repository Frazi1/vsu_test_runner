using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class QuestionTemplateController: BaseApiController
    {
        private readonly TemplateService _templateService;

        public QuestionTemplateController(TemplateService templateService)
        {
            _templateService = templateService;
        }

        [HttpGet("{id}")]
        public async Task<QuestionTemplateDto> Get(int id)
        {
            return await _templateService.GetQuestionTemplateByIdAsync(id);
        }

        [HttpPost]
        public async Task<int> Add([FromBody] QuestionTemplateDto question)
        {
            return await _templateService.AddQuestionAsync(question);
        }
    }
}