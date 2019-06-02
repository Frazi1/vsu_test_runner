using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using DataAccess.Model;
using DataAccess.Repository;
using JetBrains.Annotations;
using SharedModels.DTOs;
using SharedModels.Enum;

namespace BusinessLayer.Services
{
    [UsedImplicitly]
    public class TemplateService : BaseService
    {
        private readonly TestTemplateRepository _repository;
        private readonly CodeService _codeService;

        public TemplateService(
            TestTemplateRepository repository,
            CodeService codeService)
        {
            _repository = repository;
            _codeService = codeService;
        }

        public async Task<TestTemplateDto> GetTemplateByIdAsync(int id)
        {
            var dbTemplate = await _repository.GetFullByIdAsync(id);
            var res = dbTemplate.ToTestTemplateDto();
            return res;
        }

        public async Task<List<TestTemplateDto>> GetAllTemplatesAsync()
        {
            var dbTemplates = await _repository.GetAllFullAsync();
            var res = dbTemplates.Select(x => x.ToTestTemplateDto()).ToList();
            return res;
        }

        public async Task<TestTemplateDto> AddTestTemplateAsync(TestTemplateDto template)
        {
            var dbTemplate = template.ToDbTestTemplate();
            _repository.Add(dbTemplate);
            await _repository.SaveChangesAsync();
            await ExecuteSolutionsAndSetResults(dbTemplate);
            await _repository.SaveChangesAsync();
            return dbTemplate.ToTestTemplateDto();
        }

        private async Task ExecuteSolutionsAndSetResults(DbTestTemplate testTemplate)
        {
            foreach (var questionTemplate in testTemplate.QuestionTemplates)
            {
                var request = new CodeExecutionRequestWithCustomInputDto
                {
                    Code = questionTemplate.SolutionCodeSnippet.Code,
                    Language = LanguageIdentifier.FromString(questionTemplate.SolutionCodeSnippet.Language),
                    TestingInputs = questionTemplate.TestingInputs.Select(x => x.ToTestingInputDto()).ToList()
                };
                var taskResult = await _codeService.RunCodeForTaskResultAsync(request);
                if (taskResult.Status != CodeRunStatus.Success)
                    return;

                taskResult.ProcessRunResults.ForEach(r =>
                    questionTemplate.TestingInputs.First(i => i.Id == r.TestingInputId).ExpectedOutput = r.Output);
            }
        }

        public async Task DeleteTemplateByIdAsync(int id)
        {
            var entity = await _repository.GetByIdAsync(id);
            _repository.Remove(entity);
            await _repository.SaveChangesAsync();
        }

        public async Task UpdateTestTemplateAsync(TestTemplateDto template)
        {
            var dbTestTemplate = template.ToDbTestTemplate();
            await _repository.Update(dbTestTemplate);
            await _repository.SaveChangesAsync();
            await ExecuteSolutionsAndSetResults(dbTestTemplate);
            await _repository.SaveChangesAsync();
        }
    }
}