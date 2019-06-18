using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class UserService : BaseService
    {
        private readonly UserRepository _userRepository;

        public UserService(
            ICurrentUser currentUser,
            UserRepository userRepository)
            : base(currentUser)
        {
            _userRepository = userRepository;
        }

        public async Task<List<UserDto>> GetAllAsync()
        {
            var dbUsers = await _userRepository.GetAllAsync();
            var dtos = dbUsers.Select(u => u.ToUserDto()).ToList();
            return dtos;
        }

        public List<string> GetUserProperties()
        {
            return typeof(UserDto)
                .GetProperties(BindingFlags.Public | BindingFlags.Instance)
                .Select(p => p.Name)
                .ToList();
        }
    }
}