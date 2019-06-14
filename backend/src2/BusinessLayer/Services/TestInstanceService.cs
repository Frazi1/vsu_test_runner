using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
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
            ICurrentUser currentUser,
            TestInstanceRepository testInstanceRepository,
            TestTemplateRepository testTemplateRepository)
            : base(currentUser)
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

        public async Task UpdateTestInstanceByIdAsync(int id, TestInstanceDto dto)
        {
            var dbTestInstance = await _testInstanceRepository.GetTestInstanceWithAssigneesByIdAsync(id);
            _testInstanceRepository.Update(dbTestInstance,
                dto.Assignees.Where(a => a.User != null).Select(a => a.User.Id).ToImmutableList(),
                dto.Assignees.Where(a => a.Group != null).Select(a => a.Group.Id).ToImmutableList());
            await _testInstanceRepository.SaveChangesAsync();
        }
    }
}