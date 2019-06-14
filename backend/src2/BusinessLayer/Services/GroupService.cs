using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;
using Utils;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class GroupService : BaseService
    {
        private readonly GroupRepository _groupRepository;
        private readonly UserRepository _userRepository;

        public GroupService(
            ICurrentUser currentUser,
            GroupRepository groupRepository,
            UserRepository userRepository)
            : base(currentUser)
        {
            _groupRepository = groupRepository;
            _userRepository = userRepository;
        }

        public async Task<List<GroupDto>> GetAllAsync()
        {
            var dbGroups = await _groupRepository.GetAllWithUsersAsync();
            var dtos = dbGroups.Select(g => g.ToGroupDto()).ToList();
            return dtos;
        }

        public async Task<GroupDto> AddAsync(GroupDto group)
        {
            var dbGroup = group.ToDbGroup();

            var groupUserIds = group.Users.OrEmptyCollection()
                .Select(u => u.Id)
                .ToList();
            var users = (await _userRepository.GetByIdsAsync(groupUserIds)).ToImmutableDictionary(u => u.Id);

            var groupUsers = groupUserIds
                .Select(id => new DbUserToGroup {UserId = id, User = users[id]})
                .ToList();

            groupUsers.ForEach(u => dbGroup.Users.Add(u));

            _groupRepository.Add(dbGroup);
            await _groupRepository.SaveChangesAsync();

            return dbGroup.ToGroupDto();
        }
    }
}