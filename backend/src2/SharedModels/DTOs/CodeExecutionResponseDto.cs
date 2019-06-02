using SharedModels.Enum;

namespace SharedModels.DTOs
{
    public class CodeExecutionResponseDto
    {
        public string ActualInput { get; set; }
        public string ActualOutput { get; set; }
        public string ExpectedOutput { get; set; }
        public bool? IsValid { get; set; }
        public CodeRunStatus Status { get; set; }

        public CodeExecutionResponseDto(string actualInput, string actualOutput, bool? isValid, CodeRunStatus status)
        {
            ActualInput = actualInput;
            ActualOutput = actualOutput;
            IsValid = isValid;
            Status = status;
        }

        public CodeExecutionResponseDto(string actualInput, string actualOutput, string expectedOutput, bool? isValid, CodeRunStatus status)
        {
            ActualInput = actualInput;
            ActualOutput = actualOutput;
            ExpectedOutput = expectedOutput;
            IsValid = isValid;
            Status = status;
        }
    }
}