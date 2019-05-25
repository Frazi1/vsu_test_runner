using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using AutoMapper;
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

        public TemplateService(TestTemplateRepository repository, IMapper mapper)
            : base(mapper)
        {
            _repository = repository;
        }

        public async Task<TestTemplateDto> GetTemplateByIdAsync(int id)
        {
            var dbTemplate = await _repository.GetByIdAsync(id);
            var res = Mapper.Map<TestTemplateDto>(dbTemplate);
            return res;
        }

        public async Task<List<TestTemplateDto>> GetAllTemplatesAsync()
        {
            var dbTemplates = await _repository.GetAllAsync();
            var res = dbTemplates.Select(x => Mapper.Map<TestTemplateDto>(x)).ToList();
            return res;
        }

        public async Task<TestTemplateDto> AddTestTemplateAsync(TestTemplateDto template)
        {
            var dbTemplate = Mapper.Map<DbTestTemplate>(template);
            _repository.Add(dbTemplate);
            await _repository.SaveChangesAsync();
            return Mapper.Map<TestTemplateDto>(dbTemplate);
        }

        public async Task DeleteTemplateByIdAsync(int id)
        {
            var entity = await _repository.GetByIdAsync(id);
            _repository.Remove(entity);
            await _repository.SaveChangesAsync();
        }
    }
}