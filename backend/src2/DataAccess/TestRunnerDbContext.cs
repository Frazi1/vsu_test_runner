using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using DataAccess.Model;
using Microsoft.EntityFrameworkCore;
using JetBrains.Annotations;
using Utils;

namespace DataAccess
{
    [UsedImplicitly]
    public class TestRunnerDbContext : DbContext
    {
        public DbSet<DbTestTemplate> TestTemplates { get; set; }
        public DbSet<DbQuestionTemplate> QuestionTemplates { get; set; }
        public DbSet<DbTestingInput> TestingInputs { get; set; }
        public DbSet<DbCodeSnippet> CodeSnippets { get; set; }
        public DbSet<DbTestInstance> TestInstances { get; set; }
        public DbSet<DbQuestionInstance> QuestionInstances { get; set; }
        public DbSet<DbTestRun> TestRuns { get; set; }
        public DbSet<DbQuestionAnswer> QuestionAnswers { get; set; }
        public DbSet<DbUser> Users { get; set; }
        public DbSet<DbCodeRunIteration> CodeRunIterations { get; set; }
        public DbSet<DbInputGenerator> InputGenerators { get; set; }

        public TestRunnerDbContext(DbContextOptions options) : base(options)
        {
//            Database.EnsureDeleted();
            Database.EnsureCreated();
        }

        public override Task<int> SaveChangesAsync(bool acceptAllChangesOnSuccess,
            CancellationToken cancellationToken = new CancellationToken())
        {
            ChangeTracker.Entries()
                .Where(e => e.State == EntityState.Added)
                .Select(e => e.Entity)
                .OfType<ITimeTrackingEntity>()
                .ForEach(e => e.CreatedAt = DateTime.UtcNow);

            ChangeTracker.Entries()
                .Where(e => e.State == EntityState.Modified)
                .Select(e => e.Entity)
                .OfType<ITimeTrackingEntity>()
                .ForEach(e => e.ModifiedAt = DateTime.UtcNow);

            return base.SaveChangesAsync(acceptAllChangesOnSuccess, cancellationToken);
        }
    }
}