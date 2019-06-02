using System;
using Hangfire;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class SchedulingService : BaseService
    {
        private readonly IBackgroundJobClient _jobs;

        public SchedulingService(IBackgroundJobClient jobs)
        {
            _jobs = jobs;
        }

        public void ScheduleTestRunCompletion(int testRunId, int timeLimit)
        {
            var completeIn = TimeSpan.FromSeconds(timeLimit).Add(TimeSpan.FromMinutes(1));
            _jobs.Schedule<TestRunService>(
                x => x.FinishTestRunAsync(testRunId, Array.Empty<QuestionAnswerUpdateDto>()),
                completeIn);
        }
    }
}