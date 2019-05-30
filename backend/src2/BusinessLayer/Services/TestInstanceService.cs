using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class TestInstanceService : BaseService
    {
        private readonly TestInstanceRepository _testInstanceRepository;
        private readonly TestTemplateRepository _testTemplateRepository;

        public TestInstanceService(
            TestInstanceRepository testInstanceRepository,
            TestTemplateRepository testTemplateRepository)
        {
            _testInstanceRepository = testInstanceRepository;
            _testTemplateRepository = testTemplateRepository;
        }

        public async Task<List<TestInstanceDto>> GetAllAsync()
        {
            var dbTestInstances = await _testInstanceRepository.GetTestsInstancesWithTemplates();
            var dtos = dbTestInstances.Select(x => x.ToTestInstanceDto()).ToList();
            return dtos;
        }

        public async Task<int> CreateTestInstanceByIdAsync(int testTemplateId)
        {
            var dbTestInstance = new DbTestInstance {TestTemplateId = testTemplateId};
            var dbTestTemplate = await _testTemplateRepository.GetFullByIdAsync(testTemplateId);
            dbTestInstance.QuestionInstances = dbTestTemplate.QuestionTemplates
                .Select(t => new DbQuestionInstance {QuestionTemplateId = t.Id})
                .ToList();
            
            _testInstanceRepository.Add(dbTestInstance);
            await _testInstanceRepository.SaveChangesAsync();
            return dbTestInstance.Id;
        }

        public async Task<TestInstanceDto> GetTestInstanceByIdAsync(int id)
        {
            var dbTestInstance = await _testInstanceRepository.GetTestsInstanceWithTemplateByIdAsync(id);
            return dbTestInstance.ToTestInstanceDto();
        }
    }
}