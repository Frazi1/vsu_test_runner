﻿using System.Collections.Generic;

namespace DataAccess.Model
{
    public class DbTestTemplate: IEntityWithId
    {
        public DbTestTemplate()
        {
            QuestionTemplates = new List<DbTestTemplateToQuestion>();
            Permissions = new HashSet<DbTestTemplateUserPermission>();
            TestInstances = new HashSet<DbTestInstance>();
        }

        public int Id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int TimeLimit { get; set; }

        public virtual ICollection<DbTestTemplateToQuestion> QuestionTemplates { get; set; }
        public virtual ICollection<DbTestTemplateUserPermission> Permissions { get; set; }
        public virtual ICollection<DbTestInstance> TestInstances { get; set; }
    }
}