using System;
using System.Collections.Generic;

namespace SharedModels.DTOs
{
    public class TestRunDto
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public int TimeLimit { get; set; }
        public DateTime StartedAt { get; set; }
        public DateTime EndsAt { get; set; }
        public DateTime? FinishedAt { get; set; }
        public List<QuestionAnswerDto> QuestionAnswers { get; set; }
    }
}