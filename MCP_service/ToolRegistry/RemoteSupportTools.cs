using System.ComponentModel;
using System.Net.Http;
using System.Net.Http.Json;
using ModelContextProtocol.Server;

namespace MCP_service.ToolRegistry;

[McpServerToolType]
public static class RemoteSupportTools
{
    private static readonly HttpClient client = new()
    {
        BaseAddress = new Uri("https://support-tools.internal/api/"),
    };

    [McpServerTool, Description("Get status of a ticket from remote support system.")]
    public static async Task<string> GetRemoteTicketStatus(
        [Description("Ticket ID")] string ticketId
    )
    {
        var response = await client.GetStringAsync($"tickets/{ticketId}/status");
        return $"Remote Support Status: {response}";
    }
}
