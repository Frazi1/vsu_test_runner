namespace BusinessLayer.Executors
{
    public class ExecutionResult
    {
        public int Id { get; set; }
        public string Input { get; set; }
        public string Output { get; set; }

        public ExecutionResult(int id, string input, string output)
        {
            Id = id;
            Input = input;
            Output = output;
        }
    }
}