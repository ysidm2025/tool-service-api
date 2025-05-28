// Services/ToolDatabaseLoader.cs
// File: Services/ToolDatabaseLoader.cs
using System.Data;
using MySql.Data.MySqlClient;
using ModelContextProtocol; // or the actual namespace that defines IMcpServerTool
using MyDotNetApi.Tools; // Update based on your actual project structure


namespace MyDotNetApi.Services;

public class ToolDatabaseLoader
{
    private readonly string _connectionString;

    public ToolDatabaseLoader(string connectionString)
    {
        _connectionString = connectionString;
    }

    public async Task<List<IMcpServerTool>> LoadDynamicToolsAsync()
    {
        var tools = new List<IMcpServerTool>();

        using var conn = new MySqlConnection(_connectionString);
        await conn.OpenAsync();

        var cmd = new MySqlCommand("SELECT name, description, code FROM tools", conn);
        using var reader = await cmd.ExecuteReaderAsync();

        while (await reader.ReadAsync())
        {
            string name = reader.GetString("name");
            string description = reader.GetString("description");
            string code = reader.GetString("code");

            tools.Add(new DynamicTool(name, description, code));
        }

        return tools;
    }
}
