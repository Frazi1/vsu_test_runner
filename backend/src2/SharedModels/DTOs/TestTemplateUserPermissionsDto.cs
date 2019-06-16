namespace SharedModels.DTOs
{
    public class TestTemplateUserPermissionsDto: Permission
    {
        public int UserId { get; set; }
        public int TestTemplateId { get; set; }
        
        public UserDto User { get; set; }
    }
}