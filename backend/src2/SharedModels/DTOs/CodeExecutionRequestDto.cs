using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class CodeExecutionRequestDto
    {
        public LanguageIdentifier Language { get; set; }
        public string Code { get; set; }
    }

    public class CodeExecutionRequestWithCustomInputDto: CodeExecutionRequestDto
    {
        public List<TestingInputDto> TestingInputs { get; set; }        
    }
}