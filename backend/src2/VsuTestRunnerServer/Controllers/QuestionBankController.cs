using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class QuestionBankController : BaseApiController
    {
        private readonly QuestionBankService _questionBankService;

        public QuestionBankController(QuestionBankService questionBankService)
        {
            _questionBankService = questionBankService;
        }

        [HttpGet("")]
        [AllowAnonymous]
        public async Task<List<QuestionBankSectionDto>> GetSectionsWithQuestions(bool includeClosed = true,
            bool includeDeleted = false)
        {
            return await _questionBankService.GetSectionsWithQuestions2Async(includeClosed, includeDeleted);
        }

        [HttpGet("headers")]
        [AllowAnonymous]
        public async Task<List<QuestionBankSectionDto>> GetSectionHeaders()
        {
            return await _questionBankService.GetSectionHeadersAsync();
        }

        [HttpPost]
        public async Task<int> AddSection([FromBody] QuestionBankSectionDto section)
        {
            return await _questionBankService.AddSectionAsync(section);
        }
    }
}