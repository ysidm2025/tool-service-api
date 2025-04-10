using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;

[ApiController]
[Route("[controller]")]
public class ApiController : ControllerBase
{
    private readonly ToolService _toolService;

    public ApiController(ToolService toolService)
    {
        _toolService = toolService;
    }

    [HttpGet("bot_capabilities")]
    public ActionResult<IEnumerable<ToolMetadata>> GetCapabilities()
    {
        try
        {
            Console.WriteLine("Bot Capabilities Endpoint Hit");
            return Ok(_toolService.GetToolMetadata());
        }
        catch (Exception ex)
        {
            return StatusCode(500, ex.Message);
        }
    }

    [HttpPost("bot_response")]
    public ActionResult<string> BotResponse([FromBody] ToolRequest request)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(request.ToolName))
            {
                return BadRequest("Tool name is required.");
            }

            var parameters = request.ToolParameters ?? new Dictionary<string, string>();
            return Ok(_toolService.RunTool(request.ToolName, parameters));
        }
        catch (Exception ex)
        {
            return StatusCode(500, ex.Message);
        }
    }
}
