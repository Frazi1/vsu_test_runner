using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class GroupDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }

        public int? ParentGroupId { get; set; }

        public GroupDto ParentGroup { get; set; }
        public virtual List<UserDto> Users { get; set; }
    }
}