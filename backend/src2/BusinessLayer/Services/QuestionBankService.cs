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

        public async Task<List<QuestionBankSectionDto>> GetSectionsWithQuestions2Async(bool includeClosed, bool includeDeleted)
        {
            var defaultSection = new QuestionBankSectionDto(-1, "Default", null, null)
            {
                QuestionTemplates = (
                        await _questionTemplateRepository.GetAllAsync(q =>
                            (includeClosed || q.IsOpen) && q.QuestionBankSectionId == null &&(includeDeleted || !q.IsDeleted) ))
                    .Select(q => q.ToQuestionTemplateDto())
                    .ToList()
            };

            var sections = await _questionBankSectionRepository.GetWithQuestionHeadersAsync(includeClosed, includeDeleted);
            var res = sections
                .Select(s => s.ToQuestionBankSectionDto())
                .Prepend(defaultSection);
            return res.ToList();
        }


        public async Task<int> AddSectionAsync(QuestionBankSectionDto section)
        {
            var dbSection = new DbQuestionBankSection {Name = section.Name};
            _questionBankSectionRepository.Add(dbSection);
            await _questionTemplateRepository.SaveChangesAsync();
            return dbSection.Id;
        }
    }
}