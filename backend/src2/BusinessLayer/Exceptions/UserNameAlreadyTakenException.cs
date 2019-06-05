namespace BusinessLayer.Exceptions
{
    public class UserNameAlreadyTakenException : BusinessException
    {
        public UserNameAlreadyTakenException(string message) : base(message)
        {
        }
    }
}