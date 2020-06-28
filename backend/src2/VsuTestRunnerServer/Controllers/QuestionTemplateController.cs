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

        [HttpPut("{id}")]
        public async Task Update(int id, [FromBody] QuestionTemplateDto question)
        {
            await _templateService.UpdateQuestionTemplateAsync(id, question);
        }

        [HttpDelete("{id}")]
        public async Task Delete(int id)
        {
            await _templateService.DeleteQuestionTemplateAsync(id);
        }
    }
}