using System;
using DataAccess.Model;
using Microsoft.EntityFrameworkCore;
using JetBrains.Annotations;

namespace DataAccess
{
    [UsedImplicitly]
    public class TestRunnerDbContext : DbContext
    {
        public DbSet<DbTestTemplate> TestTemplates { get; set; }
        public DbSet<DbQuestionTemplate> QuestionTemplates { get; set; }

        public TestRunnerDbContext(DbContextOptions options) : base(options)
        {
            Database.EnsureDeleted();
            Database.EnsureCreated();
        }
    }
}