using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using JetBrains.Annotations;
using LDAPServices;
using SharedModels.DTOs;
using Utils.Helpers;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class LdapIntegrationService : BaseService
    {
        public LdapIntegrationService(ICurrentUser currentUser) 
            : base(currentUser)
        {
        }

        public async Task<List<UserDto>> SearchForUsers(ActiveDirectorySearchRequestDto request)
        {
            var conn = Connect(request);

            var attrsToQuery = request.UserFieldToActiveDirectoryAttributeMapping.Values.ToArray();
            var results = conn.GetUsers(request.BaseSearch, request.FilterQuery, attrsToQuery).ToImmutableList();
            var users = results.Select(r =>
            {
                var user = new UserDto();
                foreach (var kvp in request.UserFieldToActiveDirectoryAttributeMapping)
                {
                    var attrValue = r.getAttribute(kvp.Value);
                    user.SetPropertyValue(kvp.Key, attrValue);
                }

                return user;
            }).ToList();

            return users;
        }

        private static Query Connect(ActiveDirectorySearchRequestDto request)
            => new Query(
                request.ConnectionData.Host,
                request.ConnectionData.Port,
                request.ConnectionData.DistinguishedName,
                request.ConnectionData.Password);
    }
}