using System;
using System.Collections.Generic;
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
    public class TestRunService : BaseService
    {
        private readonly TestRunRepository _testRunRepository;
        private readonly TestInstanceRepository _testInstanceRepository;
        private readonly CodeService _codeService;
        private readonly SchedulingService _schedulingService;

        public TestRunService(ICurrentUser currentUser,
            TestRunRepository testRunRepository,
            TestInstanceRepository testInstanceRepository,
            CodeService codeService,
            SchedulingService schedulingService) : base(currentUser)
        {
            _testRunRepository = testRunRepository;
            _testInstanceRepository = testInstanceRepository;
            _codeService = codeService;
            _schedulingService = schedulingService;
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
                CodeSnippet = new DbCodeSnippet {Language = q.QuestionTemplate.SolutionCodeSnippet.Language}
            }).ToList();

            var dbTestRun = new DbTestRun
            {
                TestInstanceId = testInstanceId,
                QuestionAnswers = dbQuestionAnswers
            };
            _testRunRepository.Add(dbTestRun);
            await _testRunRepository.SaveChangesAsync();

            _schedulingService.ScheduleTestRunCompletion(dbTestRun.Id, dbTestRun.TestInstance.TestTemplate.TimeLimit);
            return dbTestRun.Id;
        }

        public async Task<TestRunDto> GetActiveTestRunByIdAsync(int id)
        {
            var dbTestRun = await _testRunRepository.GetFullByIdAsync(id);
            return dbTestRun.ToTestRunDto();
        }

        public async Task UpdateTestRunAnswersAsync(int testRunId, List<QuestionAnswerUpdateDto> answerUpdates)
        {
            var dbTestRun = await _testRunRepository.GetFullByIdAsync(testRunId);
            await UpdateTestRunAnswerInternalAsync(dbTestRun, answerUpdates);
            await _testRunRepository.SaveChangesAsync();
        }

        private async Task UpdateTestRunAnswerInternalAsync(DbTestRun dbTestRun,
            IReadOnlyCollection<QuestionAnswerUpdateDto> answerUpdates)
        {
            foreach (var answerUpdate in answerUpdates ?? Enumerable.Empty<QuestionAnswerUpdateDto>())
            {
                var dbQuestionAnswer = dbTestRun.QuestionAnswers.First(a => a.Id == answerUpdate.AnswerId);
                dbQuestionAnswer.CodeSnippet.Code = answerUpdate.AnswerCodeSnippet.Code;
                dbQuestionAnswer.CodeSnippet.Language = answerUpdate.AnswerCodeSnippet.Language.Id;
            }

            await _testRunRepository.Update(dbTestRun);
        }

        public async Task FinishTestRunAsync(int testRunId, IReadOnlyCollection<QuestionAnswerUpdateDto> answerUpdates)
        {
            var dbTestRun = await _testRunRepository.GetFullByIdAsync(testRunId);
            if(dbTestRun.FinishedAt.HasValue) return;

            await UpdateTestRunAnswerInternalAsync(dbTestRun, answerUpdates);
            await _testRunRepository.SaveChangesAsync();
            
            foreach (var dbQuestionAnswer in dbTestRun.QuestionAnswers)
            {
                dbQuestionAnswer.CodeRunIterations.Clear();
                var taskResult = await _codeService.RunQuestionTestingSetAsync(dbQuestionAnswer.Id,
                    new CodeExecutionRequestDto
                    {
                        Code = dbQuestionAnswer.CodeSnippet.Code,
                        Language = LanguageIdentifier.FromString(dbQuestionAnswer.CodeSnippet.Language)
                    });
                dbQuestionAnswer.CodeRunIterations =
                    taskResult.ProcessRunResults.Select(x => x.ToCodeRunIteration()).ToList();
                dbQuestionAnswer.ValidatedAt = DateTime.UtcNow;
                dbQuestionAnswer.ValidationPassed = dbQuestionAnswer.CodeRunIterations.All(i => i.IsValid == true);
            }

            dbTestRun.FinishedAt = DateTime.UtcNow;

            await _testRunRepository.Update(dbTestRun);
            await _testRunRepository.SaveChangesAsync();
        }

        public async Task<TestRunDto> GetFinishedTestRunByIdAsync(int id)
        {
            var dbTestRun = await _testRunRepository.GetFullByIdAsync(id);
            if (dbTestRun.FinishedAt == null)
                throw new TestRunIsNotFinishedException($"Test run {dbTestRun.Id} is not finished yet!");

            return dbTestRun.ToTestRunDto();
        }
    }
}