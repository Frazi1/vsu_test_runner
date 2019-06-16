using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using SharedModels.Enum;

namespace SharedModels.DTOs
{
    public class UserDto
    {
        public int Id { get; set; }
        public string Email { get; set; }
        public string UserName { get; set; }

        [JsonConverter(typeof(StringEnumConverter))]
        public UserType Type { get; set; }

        public List<GroupDto> Groups { get; set; }
    }
}