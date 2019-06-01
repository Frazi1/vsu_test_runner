namespace BusinessLayer.Validators
{
    public interface ITestValidator
    {
        bool Validate(string actual, string expected);
    }
}