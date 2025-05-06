using System.ComponentModel;
using ModelContextProtocol.Server;

namespace McpToolHub.Tools;

[McpServerToolType]
public static class FinanceTools
{
    [McpServerTool, Description("Get outstanding balance for resident.")]
    public static string GetOutstandingBalance([Description("Resident ID")] string residentId)
    {
        return $"Resident {residentId} has an outstanding balance of $1,245.67.";
    }
}
