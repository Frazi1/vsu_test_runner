using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class GroupService : BaseService
    {
        private readonly GroupRepository _groupRepository;

        public GroupService(
            ICurrentUser currentUser,
            GroupRepository groupRepository)
            : base(currentUser)
        {
            _groupRepository = groupRepository;
        }

        public async Task<List<GroupDto>> GetAllAsync()
        {
            var dbGroups = await _groupRepository.GetAllAsync();
            var dtos = dbGroups.Select(g => g.ToGroupDto()).ToList();
            return dtos;
        }

        public async Task<GroupDto> AddAsync(GroupDto group)
        {
            var dbGroup = group.ToDbGroup();
            _groupRepository.Add(dbGroup);
            await _groupRepository.SaveChangesAsync();

            return dbGroup.ToGroupDto();
        }
    }
}