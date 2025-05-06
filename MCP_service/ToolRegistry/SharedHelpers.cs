using System;

namespace MCP_service.ToolRegistry;

public static class SharedHelpers
{
    public static string FormatCurrency(decimal value) => $"${value:N2}";
}
