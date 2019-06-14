using System;
using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class TestInstanceDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public DateTime CreatedAt { get; set; }
        public DateTime? AvailableAfter { get; set; }
        public DateTime? DisabledAfter { get; set; }
        
        public List<QuestionInstanceDto> Questions { get; set; }
        public List<TestInstanceAssigneeDto> Assignees { get; set; }
    }
}