﻿using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbTestTemplate: IEntityWithId
    {
        public DbTestTemplate()
        {
            QuestionTemplates = new List<DbQuestionTemplate>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int TimeLimit { get; set; }

        public virtual ICollection<DbQuestionTemplate> QuestionTemplates { get; set; }
    }
}