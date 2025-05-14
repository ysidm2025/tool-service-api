using System.Reflection;
using MyDotNetApi.Models;
using MyDotNetApi.Tools;

namespace MyDotNetApi.Services
{
    public class ToolService
    {
        private readonly Dictionary<string, Type> _toolTypes = new();

        public ToolService()
        {
            var toolTypes = Assembly.GetExecutingAssembly()
                .GetTypes()
                .Where(t => t.GetCustomAttribute<FunctionToolAttribute>() != null);

            foreach (var type in toolTypes)
            {
                var attr = type.GetCustomAttribute<FunctionToolAttribute>();
                _toolTypes[attr.Name] = type;
            }
        }

        public List<ToolMetadata> GetAllTools()
        {
            return _toolTypes.Select(kvp =>
            {
                var method = kvp.Value.GetMethod("RunAsync");
                var parameters = method.GetParameters().Select(p => new ParameterMetadata
                {
                    Name = p.Name,
                    Type = p.ParameterType.Name
                }).ToList();

                var attr = kvp.Value.GetCustomAttribute<FunctionToolAttribute>();
                return new ToolMetadata
                {
                    Name = attr.Name,
                    Description = attr.Description,
                    Parameters = parameters
                };
            }).ToList();
        }

        public async Task<string> ExecuteToolAsync(string toolName, Dictionary<string, object> parameters)
        {
            if (!_toolTypes.ContainsKey(toolName))
                throw new KeyNotFoundException($"Tool '{toolName}' not found.");

            var toolType = _toolTypes[toolName];
            var method = toolType.GetMethod("RunAsync");
            var args = method.GetParameters().Select(p =>
            {
                if (!parameters.TryGetValue(p.Name, out var value))
                    throw new ArgumentException($"Missing parameter: {p.Name}");

                return Convert.ChangeType(value, p.ParameterType);
            }).ToArray();

            var result = await (Task<string>)method.Invoke(null, args);
            return result;
        }
    }
}
