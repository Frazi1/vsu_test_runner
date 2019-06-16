using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;
using SharedModels.Extensions;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class PermissionsService : BaseService
    {
        private readonly TestUserPermissionsRepository _testUserPermissionsRepository;

        public PermissionsService(ICurrentUser currentUser,
            TestUserPermissionsRepository testUserPermissionsRepository) : base(currentUser)
        {
            _testUserPermissionsRepository = testUserPermissionsRepository;
        }

        public async Task<List<TestTemplateUserPermissionsDto>> GetPermissionsForTestTemplateAsync(int templateId)
        {
            var dbPermissions = await _testUserPermissionsRepository.GetByTestTemplateIdAsync(templateId);
            var dtos = dbPermissions.Select(p => p.ToTestTemplateUserPermissionDto()).ToList();
            return dtos;
        }

        public async Task UpdatePermissionsForTestTemplateAsync(int templateId, List<TestTemplateUserPermissionsDto> permissions)
        {
            var permissionDict = permissions.ToImmutableDictionary(p => p.UserId);
            var existingPermissions = await _testUserPermissionsRepository.GetByTestTemplateIdAsync(templateId);
            foreach (var p in existingPermissions)
            {
                permissionDict[p.UserId].CopyPermissionsTo(p);
                await _testUserPermissionsRepository.Update(p);                
            }
            var newPermissions = permissionDict
                .Where(p => existingPermissions.All(ep => ep.UserId != p.Key))
                .Select(p => p.Value)
                .Select(p => p.ToDbTestTemplateUserPermission())
                .ToImmutableList();
            
            _testUserPermissionsRepository.AddRange(newPermissions);
            await _testUserPermissionsRepository.SaveChangesAsync();
        }
    }
}