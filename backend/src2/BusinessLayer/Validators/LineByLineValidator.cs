namespace BusinessLayer.Validators
{
    public class LineByLineValidator : ITestValidator
    {
        public bool Validate(string actual, string expected)
        {
            return actual == expected;
        }
    }
}