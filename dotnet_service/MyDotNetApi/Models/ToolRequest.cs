using System.Text.Json.Serialization;

public class ToolRequest
{
    [JsonPropertyName("tool_name")]
    public string? ToolName { get; set; }

    [JsonPropertyName("tool_parameters")]
    public Dictionary<string, string>? ToolParameters { get; set; }
}
