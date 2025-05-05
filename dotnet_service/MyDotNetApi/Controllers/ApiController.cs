using Microsoft.AspNetCore.Mvc;
using MyDotNetApi.Models;
using MyDotNetApi.Services;

namespace MyDotNetApi.Controllers
{
    [ApiController]
    [Route("/")]
    public class ApiController : ControllerBase
    {
        private readonly ToolService _toolService;
        private readonly OpenAIAgentService _agentService;

        public ApiController(ToolService toolService, OpenAIAgentService agentService)
        {
            _toolService = toolService;
            _agentService = agentService;
        }

        [HttpGet("bot_capabilities")]
        public IActionResult GetBotCapabilities()
        {
            var tools = _toolService.GetAllTools();
            return Ok(tools);
        }

        [HttpPost("bot_response")]
        public async Task<IActionResult> ExecuteTool([FromBody] ToolExecutionRequest request)
        {
            try
            {
                var result = await _toolService.ExecuteToolAsync(request.ToolName, request.Parameters);
                return Ok(new { result });
            }
            catch (KeyNotFoundException ex)
            {
                return NotFound(new { error = ex.Message });
            }
            catch (ArgumentException ex)
            {
                return BadRequest(new { error = ex.Message });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = "Internal error", details = ex.Message });
            }
        }

        [HttpPost("ask_agent")]
        public async Task<IActionResult> AskAgent([FromBody] AgentQueryRequest request)
        {
            var response = await _agentService.AskAgentAsync(request.Query);
            return Ok(new { response });
        }
    }
}
