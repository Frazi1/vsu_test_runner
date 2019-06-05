using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using BusinessLayer.Authentication;
using BusinessLayer.Executors;
using BusinessLayer.Executors.PipelineTasks;
using BusinessLayer.Validators;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;
using SharedModels.Enum;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class ValidationService : BaseService
    {
        private readonly ITestValidator _defaultValidator;
        private IReadOnlyCollection<ITestValidator> _validators;

        public ValidationService(IReadOnlyCollection<ITestValidator> validators, ICurrentUser currentUser) 
            : base(currentUser)
        {
            _validators = validators;
            _defaultValidator = _validators.First(v => v is LineByLineValidator);
        }

        public TaskResult ValidateResponsesWithTestingInputs(TaskResult result,
            IImmutableDictionary<int, TestingInputDto> testingInputs)
        {
            if(result.Status != CodeRunStatus.Success)
                return new TaskResult(result.Status, result.Message)
                {
                    ProcessRunResults = { new ProcessRunResult(null, null, null, result.Message, result.Status)}
                };
                
            foreach (var response in result.ProcessRunResults)
            {
                if (response.Status != CodeRunStatus.Success)
                {
                    response.IsValid = false;
                }
                else
                {
                    response.IsValid = _defaultValidator.Validate(response.Output,
                        testingInputs[response.TestingInputId.Value].ExpectedOutput);
                }
            }

            return result;
        }
    }
}