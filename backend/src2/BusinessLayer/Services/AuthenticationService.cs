using System;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using BusinessLayer.Exceptions;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using Microsoft.IdentityModel.Tokens;
using SharedModels;
using SharedModels.DTOs;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class AuthenticationService : BaseService
    {
        private readonly UserRepository _userRepository;
        private readonly IJwtSigningEncodingKey _encodingKey;

        public AuthenticationService(
            UserRepository userRepository,
            IJwtSigningEncodingKey encodingKey,
            ICurrentUser currentUser)
            : base(currentUser)
        {
            _userRepository = userRepository;
            _encodingKey = encodingKey;
        }

        public async Task<AuthenticationResponseDto> AuthenticateAsync(AuthenticationRequestDto request)
        {
            var dbUser = await _userRepository.GetFirstAsync(u =>
                (u.Email == request.UserName || u.UserName == request.UserName) &&
                u.PasswordHash == request.Password);
            if (dbUser == null)
                return null;

            var claims = new[]
            {
                new Claim(ClaimTypes.Email, dbUser.Email),
                new Claim(ClaimTypes.Name, dbUser.Email),
                new Claim(CustomClaimTypes.UserId, dbUser.Id.ToString())
            };

            var token = new JwtSecurityToken(
                issuer: "TestRunnerServer",
                audience: "TestRunnerClient",
                claims: claims,
                expires: DateTime.UtcNow.AddDays(1),
                signingCredentials: new SigningCredentials(_encodingKey.GetKey(), _encodingKey.SigningAlgorithm)
            );
            string jwtToken = new JwtSecurityTokenHandler().WriteToken(token);
            return new AuthenticationResponseDto {AccessToken = jwtToken};
        }

        public async Task<bool> IsUserNameTakenAsync(string username)
        {
            return await _userRepository.AnyAsync(u => u.Email == username || u.UserName == username);
        }

        public async Task SignUp(SignUpRequestDto request)
        {
            if (await IsUserNameTakenAsync(request.Email))
            {
                throw new UserNameAlreadyTakenException(request.Email);
            }

            var dbUser = new DbUser
            {
                Email = request.Email,
                PasswordHash = request.Password
            };
            _userRepository.Add(dbUser);
            await _userRepository.SaveChangesAsync();
        }
    }
}