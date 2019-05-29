using System.Collections.Generic;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class CodeController : BaseApiController
    {
        private readonly CodeService _codeService;

        public CodeController(CodeService codeService)
        {
            _codeService = codeService;
        }
        [HttpGet("languages")]
        public List<LanguageIdentifier> GetSupportedLanguages()
        {
            return _codeService.GetSupportedLanguages();
        }

        [HttpGet("scaffold")]
        public CodeSnippetScaffoldingDto ScaffoldStartingCodeSnippet([FromQuery] string language)
        {
            return _codeService.ScaffoldStartingLanguageSnippet(LanguageIdentifier.FromString(language));
        }
    }
}