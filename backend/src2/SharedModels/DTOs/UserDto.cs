using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class UserDto
    {
        public int Id { get; set; }
        public string Email { get; set; }
        public string UserName { get; set; }

        public List<GroupDto> Groups { get; set; }

    }
}