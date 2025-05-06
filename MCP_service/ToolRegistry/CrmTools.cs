using System.ComponentModel;
using ModelContextProtocol.Server;

namespace MCP_service.ToolRegistry;

[McpServerToolType]
public static class CrmTools
{
    [McpServerTool, Description("Get lead info by email.")]
    public static string GetLeadInfo([Description("Lead email address")] string email)
    {
        return $"Lead details for {email}: John Doe, interested in 2BR, budget $2,000.";
    }
}
