using System;
using System.Linq;
using System.Reflection;
using System.ComponentModel;
using System.Collections.Generic;

public class ToolService
{
    public ToolMetadata[] GetToolMetadata()
    {
        return AppDomain.CurrentDomain.GetAssemblies()
            .SelectMany(a => a.GetTypes())
            .Where(t => t.IsSubclassOf(typeof(Tool))) // Only subclasses of Tool
            .Select(t => 
            {
                var method = t.GetMethod("Run");
                var parameters = method?.GetParameters().Select(p => p.Name ?? "").ToArray() ?? new string[0];

                var descriptionAttr = t.GetCustomAttribute<DescriptionAttribute>();
                var description = descriptionAttr != null ? descriptionAttr.Description : "No Description";

                return new ToolMetadata(t.Name, description, parameters);
            })
            .ToArray();
    }

    public string RunTool(string toolName, Dictionary<string, string> parameters)
    {
        if (string.IsNullOrEmpty(toolName)) 
            throw new ArgumentException("Tool name cannot be null or empty", nameof(toolName));

        var toolType = AppDomain.CurrentDomain.GetAssemblies()
            .SelectMany(a => a.GetTypes())
            .FirstOrDefault(t => t.Name.Equals(toolName, StringComparison.OrdinalIgnoreCase));

        if (toolType == null)
            throw new Exception("Tool not found");

        var method = toolType.GetMethod("Run");
        if (method == null)
            throw new Exception("Run method not found");

        var toolInstance = Activator.CreateInstance(toolType);
        var methodParams = method.GetParameters();

        var args = methodParams.Select(p =>
        {
            if (parameters.TryGetValue(p.Name!, out var value))
                return Convert.ChangeType(value, p.ParameterType);
            else
                throw new Exception($"Missing required parameter: {p.Name}");
        }).ToArray();

        var result = method.Invoke(toolInstance, args);
        return result?.ToString() ?? "No result returned";
    }
}
