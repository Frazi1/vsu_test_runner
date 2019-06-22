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
    public class QuestionBankService : BaseService
    {
        private readonly QuestionBankSectionRepository _questionBankSectionRepository;
        private readonly QuestionTemplateRepository _questionTemplateRepository;

        public QuestionBankService(ICurrentUser currentUser,
            QuestionBankSectionRepository questionBankSectionRepository,
            QuestionTemplateRepository questionTemplateRepository) : base(currentUser)
        {
            _questionBankSectionRepository = questionBankSectionRepository;
            _questionTemplateRepository = questionTemplateRepository;
        }

        public async Task<List<QuestionBankSectionDto>> GetSectionHeadersAsync()
        {
            var dbQuestionBankSections = await _questionBankSectionRepository.GetAllAsync();
            var dtos = dbQuestionBankSections.Select(d => d.ToQuestionBankSectionDto()).ToList();
            return dtos;
        }
        
        public async Task<List<QuestionBankSectionDto>> GetSectionsWithQuestionsAsync()
        {
            var questions = await _questionTemplateRepository.GetWithSectionsAsync();
            var defaultSection = new QuestionBankSectionDto(-1, "Default", null, null)
            {
                QuestionTemplates = questions
                    .Where(q => q.QuestionBankSectionId == null)
                    .Select(q => q.ToQuestionTemplateDto())
                    .ToList()
            };
            var res = questions
                .GroupBy(q => q.QuestionBankSection)
                .Select(g => g.Key)
                .Where(s => s != null)
                .Select(s => s.ToQuestionBankSectionDto())
                .Prepend(defaultSection);
            return res.ToList();
        }
    }
}