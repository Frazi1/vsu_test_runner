using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using BusinessLayer.Executors;
using BusinessLayer.Executors.PipelineTasks;
using BusinessLayer.Validators;
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

        public ValidationService(IReadOnlyCollection<ITestValidator> validators)
        {
            _validators = validators;
            _defaultValidator = _validators.First(v => v is LineByLineValidator);
        }

        public void ValidateResponsesWithTestingInputs(IReadOnlyCollection<ProcessRunResult> responses,
            IImmutableDictionary<int, TestingInputDto> testingInputs)
        {
            foreach (var response in responses)
            {
                if (response.Status != CodeRunStatus.Success)
                {
                    response.IsValid = false;
                }
                else
                {
                    response.IsValid = _defaultValidator.Validate(response.Output,
                        testingInputs[response.TestingInputId].ExpectedOutput);
                }
            }
        }
    }
}