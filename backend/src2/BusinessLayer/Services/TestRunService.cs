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
    public class TestRunService : BaseService
    {
        private readonly TestRunRepository _testRunRepository;
        private readonly TestInstanceRepository _testInstanceRepository;

        public TestRunService(TestRunRepository testRunRepository, TestInstanceRepository testInstanceRepository)
        {
            _testRunRepository = testRunRepository;
            _testInstanceRepository = testInstanceRepository;
        }

        public async Task<List<TestRunDto>> GetActiveTestRunsAsync()
        {
            var dbTestRuns = await _testRunRepository.GetAllFullAsync();
            return dbTestRuns.Select(x => x.ToTestRunDto()).ToList();
        }

        public async Task<int> StartTestRunFromTestInstanceAsync(int testInstanceId)
        {
            var testInstance = await _testInstanceRepository.GetTestsInstanceWithTemplateByIdAsync(testInstanceId);
            
            //TODO: set user id
            var dbQuestionAnswers = testInstance.QuestionInstances.Select(q => new DbQuestionAnswer
            {
                QuestionInstanceId = q.Id,
                CodeSnippet = new DbCodeSnippet()
            }).ToList();
            
            var dbTestRun = new DbTestRun
            {
                TestInstanceId = testInstanceId,
                QuestionAnswers = dbQuestionAnswers
            };
            _testRunRepository.Add(dbTestRun);
            await _testRunRepository.SaveChangesAsync();

            return dbTestRun.Id;
        }

        public async Task<TestRunDto> GetActiveTestRunByIdAsync(int id)
        {
            var dbTestRun = await _testRunRepository.GetFullByIdAsync(id);
            return dbTestRun.ToTestRunDto();
        }
    }
}