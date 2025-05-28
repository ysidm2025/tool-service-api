// Tools/DynamicTool.cs
using ModelContextProtocol;
using Microsoft.CodeAnalysis.CSharp.Scripting;
using Microsoft.CodeAnalysis.Scripting;

namespace MyDotNetApi.Tools;

public class DynamicTool : IMcpServerTool
{
    private readonly string _name;
    private readonly string _description;
    private readonly string _code;

    public DynamicTool(string name, string description, string code)
    {
        _name = name;
        _description = description;
        _code = code;
    }

    public string Name => _name;
    public string Description => _description;

    public async Task<object?> InvokeAsync(object? input, CancellationToken cancellationToken = default)
    {
        if (input is not string query)
            return $"Expected a string query, got: {input?.GetType().Name}";

        var script = $"{_code}\n{name}(\"{query}\");";
        try
        {
            var result = await CSharpScript.EvaluateAsync<string>(script, ScriptOptions.Default);
            return result;
        }
        catch (Exception ex)
        {
            return $"Error executing tool '{_name}': {ex.Message}";
        }
    }

    public Type InputType => typeof(string);
    public Type OutputType => typeof(string);
}
