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
        public DbSet<DbGroup> Groups { get; set; }
        public DbSet<DbTestInstanceUserAssignee> TestInstanceUserAssignees { get; set; }
        public DbSet<DbTestInstanceGroupAssignee> TestInstanceGroupAssignees { get; set; }

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

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<DbUserToGroup>()
                .HasKey(ug => new {ug.UserId, ug.GroupId});

            modelBuilder.Entity<DbUserToGroup>()
                .HasOne(ug => ug.User)
                .WithMany(u => u.Groups)
                .HasForeignKey(ug => ug.UserId);

            modelBuilder.Entity<DbUserToGroup>()
                .HasOne(ug => ug.Group)
                .WithMany(g => g.Users)
                .HasForeignKey(ug => ug.GroupId);

            modelBuilder.Entity<DbTestInstanceAssignee>().ToTable("TestInstanceAssignees")
                .HasDiscriminator<InstanceAssigneeType>("AssigneeType")
                .HasValue<DbTestInstanceUserAssignee>(InstanceAssigneeType.User)
                .HasValue<DbTestInstanceGroupAssignee>(InstanceAssigneeType.Group);

            modelBuilder.Entity<DbTestInstance>()
                .HasMany(a => a.AssignedUsers)
                .WithOne(a => a.TestInstance)
                .HasForeignKey(a => a.TestInstanceId);

            modelBuilder.Entity<DbTestInstance>()
                .HasMany(a => a.AssignedGroups)
                .WithOne(a => a.TestInstance)
                .HasForeignKey(a => a.TestInstanceId);
        }
    }
}