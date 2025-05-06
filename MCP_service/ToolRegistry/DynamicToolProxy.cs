using System.ComponentModel;
using System.Net.Http.Json;
using ModelContextProtocol.Server;

// If teams register tools in a database (e.g., name, parameters, endpoint), you can use a “proxy tool” pattern
namespace MCP_service.ToolRegistry;

[McpServerToolType]
public static class DynamicToolProxy
{
    private static readonly HttpClient client = new();

    [McpServerTool, Description("Execute a dynamic tool from the tool registry.")]
    public static async Task<string> RunDynamicTool(
        [Description("Tool name")] string toolName,
        [Description("JSON parameters (as string)")] string parameters
    )
    {
        var registryEndpoint = $"https://tool-registry.internal/run?tool={toolName}";
        var content = new StringContent(parameters, System.Text.Encoding.UTF8, "application/json");

        var response = await client.PostAsync(registryEndpoint, content);
        return await response.Content.ReadAsStringAsync();
    }
}
