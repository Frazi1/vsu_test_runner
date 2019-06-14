using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using JetBrains.Annotations;
using Microsoft.EntityFrameworkCore;
using SharedModels.DTOs;

namespace DataAccess.Repository
{
    [UsedImplicitly]
    public class TestInstanceRepository : BaseRepository<DbTestInstance>
    {
        public TestInstanceRepository(TestRunnerDbContext context) : base(context)
        {
        }

        private IQueryable<DbTestInstance> SetWithTemplates()
        {
            return Set
                .Include(d => d.TestTemplate)
                .Include(d => d.QuestionInstances)
                .ThenInclude(q => q.QuestionTemplate)
                .ThenInclude(t => t.SolutionCodeSnippet);
        }

        public async Task<DbTestInstance> GetTestInstanceWithAssigneesByIdAsync(int id)
        {
            return await Set.WithAssignees().FirstAsync(a => a.Id == id);
        }

        public async Task<List<DbTestInstance>> GetTestsInstancesWithTemplates()
        {
            return await SetWithTemplates().WithAssignees().ToListAsync();
        }

        public async Task<DbTestInstance> GetTestsInstanceWithTemplateByIdAsync(int id)
        {
            return await SetWithTemplates().WithAssignees().FirstAsync(d => d.Id == id);
        }

        public void Update(DbTestInstance entity,
            ICollection<int> newUserAssignees,
            ICollection<int> newGroupAssignees)
        {
            var deletedUsers = entity.AssignedUsers.Where(a => newUserAssignees.FirstOrDefault(i => a.UserId == i) == 0)
                .ToList();
            deletedUsers.ForEach(e => Context.Entry(e).State = EntityState.Deleted);

            var deletedGroups = entity.AssignedGroups
                .Where(a => newUserAssignees.FirstOrDefault(i => a.GroupId == i) == 0).ToList();
            deletedGroups.ForEach(e => Context.Entry(e).State = EntityState.Deleted);

            var addedUsersIds = newUserAssignees.Except(deletedUsers.Select(a => a.UserId)).ToList();
            addedUsersIds.ForEach(u => entity.AssignedUsers.Add(new DbTestInstanceUserAssignee
                {UserId = u, AssigneeType = InstanceAssigneeType.User}));
            
            var addedGroupIds = newGroupAssignees.Except(deletedGroups.Select(a => a.GroupId)).ToList();
            addedGroupIds.ForEach(g => entity.AssignedUsers.Add(new DbTestInstanceUserAssignee
                {UserId = g, AssigneeType = InstanceAssigneeType.Group}));
//            Context.Update(entity);
        }
    }

    static class TestInstanceRepositoryQueryHelper
    {
        public static IQueryable<DbTestInstance> WithAssignees(this IQueryable<DbTestInstance> q)
            => q.Include(a => a.AssignedUsers).ThenInclude(a => a.User)
                .Include(a => a.AssignedGroups).ThenInclude(a => a.Group);
    }
}