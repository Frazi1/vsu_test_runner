using DataAccess.Model;
using SharedModels.Enum;

namespace BusinessLayer.Executors.PipelineTasks
{
    public class ProcessRunResult
    {
        public int TestingInputId { get; set; }
        public string Input { get; set; }
        public string Output { get; set; }
        public string Error { get; set; }
        public CodeRunStatus Status { get; set; }

        public ProcessRunResult(int testingInputId, string input, string output, string error, CodeRunStatus status)
        {
            TestingInputId = testingInputId;
            Input = input;
            Output = output;
            Error = error;
            Status = status;
        }
    }
}