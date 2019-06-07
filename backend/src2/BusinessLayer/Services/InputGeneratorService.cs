using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using BusinessLayer.Wildcards;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class InputGeneratorService : BaseService
    {
        private readonly InputGeneratorRepository _inputGeneratorRepository;
        private readonly UserRepository _userRepository;
        private readonly WildcardsFactory _wildcardsFactory;

        public InputGeneratorService(
            ICurrentUser currentUser,
            InputGeneratorRepository inputGeneratorRepository,
            UserRepository userRepository,
            WildcardsFactory wildcardsFactory
        )
            : base(currentUser)
        {
            _inputGeneratorRepository = inputGeneratorRepository;
            _userRepository = userRepository;
            _wildcardsFactory = wildcardsFactory;
        }

        public async Task<InputGeneratorDto> GetFullByIdAsync(int id)
        {
            var dbGenerator = await _inputGeneratorRepository.GetFullByIdAsync(id);
            var dto = dbGenerator.ToInputGeneratorDto();
            return dto;
        }

        private void SetCallArguments(InputGeneratorDto generator)
        {
            var callArguments = _wildcardsFactory
                .CallParameterWildcard(generator.CodeSnippet.Language)
                .GetCallParameters(generator.CodeSnippet.Code)
                .CallArguments;

            generator.CallArguments = callArguments.ToList();
        }
        
        public async Task<InputGeneratorDto> AddAsync(InputGeneratorDto generator)
        {
            SetCallArguments(generator);
            
            var dbGenerator = generator.ToDbInputGenerator(CurrentUser.Id);
            
            _inputGeneratorRepository.Add(dbGenerator);
            await _inputGeneratorRepository.SaveChangesAsync();
            dbGenerator.CreatedByUser = await _userRepository.GetByIdAsync(CurrentUser.Id);
            return dbGenerator.ToInputGeneratorDto();
        }

        public async Task UpdateAsync(InputGeneratorDto generator)
        {
            SetCallArguments(generator);
            
            var dbUpdate = generator.ToUpdateDbInputGenerator();
            await _inputGeneratorRepository.Update(dbUpdate);
            await _inputGeneratorRepository.SaveChangesAsync();
        }

        public async Task<List<InputGeneratorDto>> GetAllAsync()
        {
            var dbGenerators = await _inputGeneratorRepository.GetAllFullAsync();
            var dtos = dbGenerators.Select(g => g.ToInputGeneratorDto()).ToList();
            return dtos;
        }
    }
}