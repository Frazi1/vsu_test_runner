namespace BusinessLayer.Authentication
{
    public interface ICurrentUser
    {
        int Id { get; }
        string Email { get; }
        string UserName { get; }
        string[] Roles { get; }
    }

    public class CurrentUser : ICurrentUser
    {
        public int Id { get; }
        public string Email { get; }
        public string UserName { get; }
        public string[] Roles { get; }

        public CurrentUser(int id, string email, string userName, string[] roles)
        {
            Id = id;
            Email = email;
            UserName = userName;
            Roles = roles;
        }
    }
}