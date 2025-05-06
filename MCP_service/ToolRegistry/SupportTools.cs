using System.ComponentModel;
using ModelContextProtocol.Server;

namespace MCP_service.ToolRegistry;

[McpServerToolType]
public static class SupportTools
{
    [McpServerTool, Description("Check the status of a support ticket.")]
    public static string GetTicketStatus([Description("Ticket ID")] string ticketId)
    {
        return $"Ticket {ticketId} is currently in progress.";
    }
}
