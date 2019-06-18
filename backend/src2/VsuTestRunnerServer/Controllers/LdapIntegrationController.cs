using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class LdapIntegrationController : BaseApiController
    {
        private readonly UserService _userService;
        private readonly LdapIntegrationService _ldapIntegrationService;

        public LdapIntegrationController(
            UserService userService,
            LdapIntegrationService ldapIntegrationService
        )
        {
            _userService = userService;
            _ldapIntegrationService = ldapIntegrationService;
        }

        [HttpGet("user_properties")]
        public List<string> GetUserProperties()
        {
            return _userService.GetUserProperties();
        }

        [HttpPost]
        public async Task<List<UserDto>> SearchADForUsers([FromBody] ActiveDirectorySearchRequestDto request)
        {
            return await _ldapIntegrationService.SearchForUsers(request);
        }
    }
}