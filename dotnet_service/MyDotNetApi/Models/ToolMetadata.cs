using System.Text.Json.Serialization;

public class ToolMetadata
{
    [JsonPropertyName("tool_name")]
    public string ToolName { get; set; }

    [JsonPropertyName("description")]
    public string Description { get; set; }

    [JsonPropertyName("parameters")]
    public string[] Parameters { get; set; }

    public ToolMetadata(string toolName, string description, string[] parameters)
    {
        ToolName = toolName;
        Description = description;
        Parameters = parameters;
    }
}
