using System.Linq;
using DataAccess.Model;
using SharedModels.DTOs;

namespace BusinessLayer
{
    public static class Mappings
    {
        public static CodeSnippetDto ToCodeSnippetDto(this DbCodeSnippet e)
            => new CodeSnippetDto
            {
                Id = e.Id,
                Code = e.Code,
                Language = LanguageIdentifier.FromString(e.Language)
            };

        public static DbCodeSnippet ToDbCodeSnippet(this CodeSnippetDto d)
            => new DbCodeSnippet
            {
                Id = d.Id,
                Code = d.Code,
                Language = d.Language.ToString()
            };

        public static TestingInputDto ToTestingInputDto(this DbTestingInput e)
            => new TestingInputDto
            {
                Id = e.Id,
                ExpectedOutput = e.ExpectedOutput,
                Input = e.Input
            };

        public static DbTestingInput ToDbTestingInput(this TestingInputDto d)
            => new DbTestingInput
            {
                Id = d.Id,
                ExpectedOutput = d.ExpectedOutput,
                Input = d.Input
            };

        public static QuestionTemplateDto ToQuestionTemplateDto(this DbQuestionTemplate e)
            => new QuestionTemplateDto
            {
                Id = e.Id,
                Name = e.Name,
                Description = e.Description,
                CodeSnippet = e.SolutionCodeSnippet.ToCodeSnippetDto(),
                TestingInputs = e.TestingInputs.Select(ToTestingInputDto).ToList()
            };

        public static DbQuestionTemplate ToDbQuestionTemplate(this QuestionTemplateDto d)
            => new DbQuestionTemplate
            {
                Id = d.Id,
                Name = d.Name,
                Description = d.Description,
                SolutionCodeSnippet = d.CodeSnippet.ToDbCodeSnippet(),
                TestingInputs = d.TestingInputs.Select(ToDbTestingInput).ToList()
            };

        public static TestTemplateDto ToTestTemplateDto(this DbTestTemplate e)
            => new TestTemplateDto
            {
                Id = e.Id,
                Description = e.Description,
                Name = e.Name,
                TimeLimit = e.TimeLimit,
                QuestionTemplates = e.QuestionTemplates.Select(ToQuestionTemplateDto).ToList()
            };

        public static DbTestTemplate ToDbTestTemplate(this TestTemplateDto d)
            => new DbTestTemplate
            {
                Id = d.Id,
                Description = d.Description,
                Name = d.Name,
                TimeLimit = d.TimeLimit,
                QuestionTemplates = d.QuestionTemplates.Select(ToDbQuestionTemplate).ToList()
            };
    }
}