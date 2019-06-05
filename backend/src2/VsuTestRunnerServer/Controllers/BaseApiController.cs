using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace VsuTestRunnerServer.Controllers
{
    [Route("api/[controller]")]
    [Authorize]
    [ApiController]
    public class BaseApiController: ControllerBase
    {
        
    }
}