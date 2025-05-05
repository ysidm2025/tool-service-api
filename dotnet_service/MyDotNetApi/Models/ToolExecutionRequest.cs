using System.Collections.Generic;

namespace MyDotNetApi.Models
{
    public class ToolExecutionRequest
    {
        public string ToolName { get; set; }
        public Dictionary<string, object> Parameters { get; set; }
    }
}
