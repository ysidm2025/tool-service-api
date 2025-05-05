using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using MyDotNetApi.Models;
using ToolParameterInfo = MyDotNetApi.Models.ParameterInfo;

namespace MyDotNetApi.Services
{
    public class ToolService
    {
        private readonly ILogger<ToolService> _logger;
        private readonly Dictionary<string, Type> _toolTypes;

        public ToolService(ILogger<ToolService> logger)
        {
            _logger = logger;
            _toolTypes = new Dictionary<string, Type>();
            DiscoverTools();
        }

        private void DiscoverTools()
        {
            var assembly = Assembly.GetExecutingAssembly();
            var toolTypes = assembly.GetTypes()
                .Where(t => t.GetCustomAttribute<FunctionToolAttribute>() != null);

            foreach (var type in toolTypes)
            {
                var attribute = type.GetCustomAttribute<FunctionToolAttribute>();
                if (attribute != null)
                {
                    _toolTypes[attribute.Name] = type;
                }
            }
        }

        public List<ToolInfo> GetAllTools()
        {
            var tools = new List<ToolInfo>();

            foreach (var (name, type) in _toolTypes)
            {
                var attribute = type.GetCustomAttribute<FunctionToolAttribute>();
                if (attribute == null) continue;

                var parameters = new List<ToolParameterInfo>();
                var method = type.GetMethod("Run");
                if (method == null) continue;

                foreach (var param in method.GetParameters())
                {
                    parameters.Add(new ToolParameterInfo
                    {
                        Name = param.Name ?? throw new InvalidOperationException($"Parameter name is null for tool {name}"),
                        Type = param.ParameterType.Name,
                        IsRequired = !param.IsOptional
                    });
                }

                tools.Add(new ToolInfo
                {
                    Name = attribute.Name,
                    Description = attribute.Description,
                    Parameters = parameters
                });
            }

            return tools;
        }

        public async Task<object> ExecuteToolAsync(string toolName, Dictionary<string, object> parameters)
        {
            if (!_toolTypes.TryGetValue(toolName, out var toolType))
            {
                throw new KeyNotFoundException($"Tool '{toolName}' not found");
            }

            var instance = Activator.CreateInstance(toolType);
            if (instance == null)
            {
                throw new InvalidOperationException($"Failed to create instance of tool '{toolName}'");
            }

            var method = toolType.GetMethod("Run") ?? throw new InvalidOperationException($"Run method not found for tool '{toolName}'");
            var methodParams = method.GetParameters();
            var paramValues = new object[methodParams.Length];

            for (int i = 0; i < methodParams.Length; i++)
            {
                var param = methodParams[i];
                var paramName = param.Name ?? throw new InvalidOperationException($"Parameter name is null for tool {toolName}");

                if (parameters.TryGetValue(paramName, out var value))
                {
                    try
                    {
                        paramValues[i] = Convert.ChangeType(value, param.ParameterType);
                    }
                    catch (Exception ex)
                    {
                        throw new ArgumentException($"Invalid value for parameter '{paramName}': {ex.Message}");
                    }
                }
                else if (param.IsOptional)
                {
                    paramValues[i] = param.DefaultValue ?? throw new InvalidOperationException($"Default value is null for optional parameter {paramName}");
                }
                else
                {
                    throw new ArgumentException($"Required parameter '{paramName}' not provided");
                }
            }

            if (method.ReturnType.IsAssignableTo(typeof(Task)))
            {
                var task = (Task)method.Invoke(instance, paramValues)!;
                await task;
                var resultProperty = task.GetType().GetProperty("Result");
                return resultProperty?.GetValue(task) ?? throw new InvalidOperationException("Task result is null");
            }

            return method.Invoke(instance, paramValues) ?? throw new InvalidOperationException("Method result is null");
        }
    }
} 