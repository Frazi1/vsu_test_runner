using AutoMapper;
using DataAccess.Model;
using JetBrains.Annotations;
using SharedModels.DTOs;

namespace BusinessLayer
{
    [UsedImplicitly]
    public class MapperProfile : Profile
    {
        public MapperProfile()
        {
            CreateMap<DbTestTemplate, TestTemplateDto>(MemberList.Destination)
                .ForMember(a => a.Id, a => a.MapFrom(rec => rec.Id))
                .ForMember(a => a.Description, a => a.MapFrom(rec => rec.Description))
                .ForMember(a => a.Name, a => a.MapFrom(rec => rec.Name))
                .ForMember(a => a.QuestionTemplates, a => a.MapFrom(rec => rec.QuestionTemplates))
                .ForMember(a => a.TimeLimit, a => a.MapFrom(rec => rec.TimeLimit))
                .ReverseMap()
                .ForAllOtherMembers(a => a.Ignore());

            CreateMap<DbQuestionTemplate, QuestionTemplateDto>(MemberList.None)
                .ReverseMap();

            CreateMap<DbCodeSnippet, CodeSnippetDto>()
                .ReverseMap();

            CreateMap<DbTestingInput, TestingInputDto>()
                .ReverseMap()
                .ForMember(a=> a.QuestionTemplateId, expression => expression.Ignore())
                ;
        }
    }
}