using System.Collections.Generic;
using System.Threading.Tasks;
using BusinessLayer.Services;
using Microsoft.AspNetCore.Mvc;
using SharedModels.DTOs;

namespace VsuTestRunnerServer.Controllers
{
    public class GroupController : BaseApiController
    {
        private readonly GroupService _groupService;

        public GroupController(GroupService groupService)
        {
            _groupService = groupService;
        }
        
        [HttpGet]
        public async Task<List<GroupDto>> GetAll()
        {
            return await _groupService.GetAllAsync();
        }

        [HttpPost]
        public async Task<int> Add([FromBody] GroupDto group)
        {
            return (await _groupService.AddAsync(group)).Id;
        }
    }
}