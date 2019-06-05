using System.Security.Authentication;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    [Route("api/auth")]
    public class AuthenticationController : BaseApiController
    {
        private readonly AuthenticationService _authenticationService;

        public AuthenticationController(AuthenticationService authenticationService)
        {
            _authenticationService = authenticationService;
        }

        [HttpPost]
        [AllowAnonymous]
        public async Task<AuthenticationResponseDto> Authenticate([FromBody] AuthenticationRequestDto request)
        {
            var authenticationResult = _authenticationService.AuthenticateAsync(request);
            if (authenticationResult == null)
                throw new InvalidCredentialException();

            return await authenticationResult;
        }

        [HttpPost("signup")]
        [AllowAnonymous]
        public async Task SignUp([FromBody] SignUpRequestDto request)
        {
            await _authenticationService.SignUp(request);
        }

        [HttpGet("check_username")]
        [AllowAnonymous]
        public async Task<bool> IsUserNameTakenAsync([FromQuery] string username)
        {
            return await _authenticationService.IsUserNameTakenAsync(username);
        }
    }
}