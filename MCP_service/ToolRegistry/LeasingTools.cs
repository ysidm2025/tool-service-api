using System.ComponentModel;
using ModelContextProtocol.Server;

namespace MCP_service.ToolRegistry;

[McpServerToolType]
public static class LeasingTools
{
    [McpServerTool, Description("Check unit availability by unit number.")]
    public static string CheckUnitAvailability(
        [Description("Unit number to check.")] string unitNumber
    )
    {
        // Replace with DB/service call
        return $"Unit {unitNumber} is currently available.";
    }
}
