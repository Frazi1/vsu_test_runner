using AutoMapper;

namespace BusinessLayer.Services
{
    public class BaseService
    {
        protected IMapper Mapper { get; }

        protected BaseService(IMapper mapper)
        {
            Mapper = mapper;
        }
    }
}