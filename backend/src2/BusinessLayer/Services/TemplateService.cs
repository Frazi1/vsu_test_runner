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
    public class TemplateService : BaseService
    {
        private readonly TestTemplateRepository _repository;

        public TemplateService(TestTemplateRepository repository)
        {
            _repository = repository;
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
            return dbTemplate.ToTestTemplateDto();
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
        }
    }
}