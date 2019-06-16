using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using BusinessLayer.Executors;
using DataAccess.Model;
using SharedModels.DTOs;
using SharedModels.Enum;
using Utils;

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

        public static TestInstanceDto ToTestInstanceDto(this DbTestInstance d)
            => new TestInstanceDto
            {
                Id = d.Id,
                Name = d.TestTemplate.Name,
                CreatedAt = d.CreatedAt,
                DisabledAfter = d.DisabledAfter,
                AvailableAfter = d.AvailableAfter,
                Questions = d.QuestionInstances.Select(ToQuestionInstanceDto).ToList(),
                Assignees = d.AssignedUsers.Select(a => a.ToTestInstanceUserAssigneeDto())
                    .Concat(d.AssignedGroups.Select(a => a.ToTestInstanceGroupAssigneeDto()))
                    .ToList()
            };

        public static QuestionInstanceDto ToQuestionInstanceDto(this DbQuestionInstance d)
            => new QuestionInstanceDto
            {
                Id = d.Id,
                Name = d.QuestionTemplate.Name
            };

        public static TestRunDto ToTestRunDto(this DbTestRun d)
            => new TestRunDto
            {
                Id = d.Id,
                Name = d.TestInstance.TestTemplate.Name,
                TimeLimit = d.TestInstance.TestTemplate.TimeLimit,
                StartedAt = d.CreatedAt,
                EndsAt = d.CreatedAt.Add(TimeSpan.FromSeconds(d.TestInstance.TestTemplate.TimeLimit)),
                FinishedAt = d.FinishedAt,
                QuestionAnswers = d.QuestionAnswers.Select(ToQuestionAnswerDto).ToList()
            };

        public static DbTestRun ToDbTestRun(this TestRunDto d)
            => new DbTestRun
            {
                Id = d.Id,
                QuestionAnswers = d.QuestionAnswers.Select(ToDbQuestionAnswer).ToList()
            };

        public static DbQuestionAnswer ToDbQuestionAnswer(this QuestionAnswerDto d)
            => new DbQuestionAnswer
            {
                Id = d.Id,
                CodeSnippet = d.AnswerCodeSnippet.ToDbCodeSnippet(),
                ValidationPassed = d.ValidationPassed
            };

        public static QuestionAnswerDto ToQuestionAnswerDto(this DbQuestionAnswer d)
            => new QuestionAnswerDto
            {
                Id = d.Id,
                Name = d.QuestionInstance.QuestionTemplate.Name,
                Iterations = d.CodeRunIterations.Select(ToCodeExecutionResponseDto).ToList(),
                Description = d.QuestionInstance.QuestionTemplate.Description,
                IsValidated = d.ValidatedAt.HasValue,
                ValidationPassed = d.ValidationPassed,
                AnswerCodeSnippet = d.CodeSnippet.ToCodeSnippetDto()
            };

        public static CodeExecutionResponseDto ToCodeExecutionResponseDto(this ProcessRunResult d)
            => new CodeExecutionResponseDto(d.Input, d.Status == CodeRunStatus.Success ? d.Output : d.Error, d.IsValid,
                d.Status);

        public static CodeExecutionResponseDto ToCodeExecutionResponseDto(this DbCodeRunIteration d)
            => new CodeExecutionResponseDto(d.TestingInput?.Input, d.ActualOutput, d.TestingInput?.ExpectedOutput,
                d.IsValid, d.Status);

        public static DbCodeRunIteration ToCodeRunIteration(this ProcessRunResult d)
            => new DbCodeRunIteration
            {
                Status = d.Status,
                TestingInputId = d.TestingInputId,
                IsValid = d.IsValid,
                ActualOutput = d.Status == CodeRunStatus.Success ? d.Output : d.Error
            };

        public static InputGeneratorDto ToInputGeneratorDto(this DbInputGenerator d)
            => new InputGeneratorDto
            {
                Id = d.Id,
                Name = d.Name,
                Description = d.Description,
                CodeSnippet = d.CodeSnippet.ToCodeSnippetDto(),
                CreatedByUser = d.CreatedByUser.Email.OrIfNullOrEmpty(d.CreatedByUser.UserName),
                CallArguments = GetGeneratorCallArguments(d.CallParameters)
            };

        public static List<GeneratorCallArgumentDto> GetGeneratorCallArguments(string input)
            => input.Split(new[] {","}, StringSplitOptions.RemoveEmptyEntries)
                .Select(item => new GeneratorCallArgumentDto {Name = item})
                .ToList();

        public static DbInputGenerator ToDbInputGenerator(this InputGeneratorDto d, int creatorUserId = 0)
        {
            var r = d.ToUpdateDbInputGenerator();
            r.CreatedByUserId = creatorUserId;
            return r;
        }

        public static DbInputGenerator ToUpdateDbInputGenerator(this InputGeneratorDto d)
            => new DbInputGenerator
            {
                Id = d.Id,
                Name = d.Name,
                Description = d.Description,
                CodeSnippet = d.CodeSnippet.ToDbCodeSnippet(),
                CodeSnippetId = (d.CodeSnippet?.Id).GetValueOrDefault(),
                CallParameters = (d.CallArguments ?? Enumerable.Empty<GeneratorCallArgumentDto>())
                    .Select(a => a.Name)
                    .JoinToString(","),
            };

        public static GroupDto ToGroupDtoWithoutUsers(this DbGroup d)
            => new GroupDto
            {
                Id = d.Id,
                Name = d.Name,
                Description = d.Description,
                ParentGroupId = d.ParentGroupId,
                ParentGroup = d.ParentGroup?.ToGroupDto()
            };


        public static GroupDto ToGroupDto(this DbGroup d)
        {
            var res = d.ToGroupDtoWithoutUsers();
            res.Users = d.Users.OrEmptyCollection()
                .Select(u => u.User.ToUserDtoWithoutGroups())
                .ToList();
            return res;
        }


        public static UserDto ToUserDtoWithoutGroups(this DbUser d)
            => new UserDto
            {
                Id = d.Id,
                Email = d.Email,
                UserName = d.UserName.OrIfNullOrEmpty(d.Email),
                Type = d.Type
            };

        public static UserDto ToUserDto(this DbUser d)
        {
            var u = d.ToUserDtoWithoutGroups();
            u.Groups = d.Groups.OrEmptyCollection().Select(g => g.Group).Select(g => g.ToGroupDto()).ToList();

            return u;
        }

        public static DbGroup ToDbGroup(this GroupDto d)
            => new DbGroup
            {
                Id = d.Id,
                Name = d.Name,
                Description = d.Description,
                ParentGroupId = d.ParentGroupId ?? d.ParentGroup?.Id
            };

        public static TestInstanceAssigneeDto ToTestInstanceAssigneeDto(this DbTestInstanceAssignee d)
        {
            switch (d.AssigneeType)
            {
                case InstanceAssigneeType.User:
                    return ToTestInstanceUserAssigneeDto((DbTestInstanceUserAssignee) d);
                case InstanceAssigneeType.Group:
                    return ToTestInstanceGroupAssigneeDto((DbTestInstanceGroupAssignee) d);
                default:
                    throw new ArgumentOutOfRangeException();
            }
        }

        private static TestInstanceAssigneeDto ToTestInstanceGroupAssigneeDto(this DbTestInstanceGroupAssignee d)
        {
            return new TestInstanceAssigneeDto
            {
                Id = d.Id,
                Group = d.Group.ToGroupDtoWithoutUsers()
            };
        }

        private static TestInstanceAssigneeDto ToTestInstanceUserAssigneeDto(this DbTestInstanceUserAssignee d)
        {
            return new TestInstanceAssigneeDto {Id = d.Id, User = d.User.ToUserDtoWithoutGroups()};
        }
    }
}