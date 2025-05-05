using System.Collections.Generic;

namespace MyDotNetApi.Models
{
    public class ToolInfo
    {
        public required string Name { get; set; }
        public required string Description { get; set; }
        public required List<ParameterInfo> Parameters { get; set; }
    }

    public class ParameterInfo
    {
        public required string Name { get; set; }
        public required string Type { get; set; }
        public bool IsRequired { get; set; }
    }
    
    public class AgentRequest
    {
        public required string Query { get; set; }
    }

    public class ApiResponse<T>
    {
        public bool Success { get; set; }
        public string? Message { get; set; }
        public T? Data { get; set; }
    }
} 