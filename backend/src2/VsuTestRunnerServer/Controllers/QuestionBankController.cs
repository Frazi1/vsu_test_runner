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
        public async Task<List<QuestionBankSectionDto>> GetSectionsWithQuestions()
        {
            return await _questionBankService.GetSectionsWithQuestionsAsync();
        }
        
        [HttpGet("headers")]
        [AllowAnonymous]
        public async Task<List<QuestionBankSectionDto>> GetSectionHeaders()
        {
            return await _questionBankService.GetSectionHeadersAsync();
        }
    }
}