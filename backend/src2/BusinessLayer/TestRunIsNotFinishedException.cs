namespace BusinessLayer
{
    public class TestRunIsNotFinishedException : BusinessException
    {
        public TestRunIsNotFinishedException(string message) : base(message)
        {
        }
    }
}