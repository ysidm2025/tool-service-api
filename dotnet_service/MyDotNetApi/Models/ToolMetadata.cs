using System.Collections.Generic;

namespace MyDotNetApi.Models
{
    public class ToolMetadata
    {
        public required string Name { get; set; }
        public required string Description { get; set; }
        public required List<ToolParameterMetadata> Parameters { get; set; }
    }

    public class ToolParameterMetadata
    {
        public required string Name { get; set; }
        public required string Type { get; set; }
    }
}
