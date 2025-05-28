// Program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using PropertyMcpServer.Tools;
using OpenTelemetry.Extensions.Hosting;
using MyDotNetApi.Services;

var builder = WebApplication.CreateBuilder(args);

string mysqlConn = builder.Configuration.GetConnectionString("MySql");

// Read MySQL connection string from appsettings or environment
string mysqlConn = builder.Configuration.GetConnectionString("MySql")
    ?? Environment.GetEnvironmentVariable("MYSQL_CONN")
    ?? "server=localhost;database=mcpdb;user=root;password=yourpass;";

// Register dynamic tool loader service
var toolLoader = new ToolDatabaseLoader(mysqlConn);
var dynamicTools = await toolLoader.LoadDynamicToolsAsync(); // Load from DB

// Register MCP server with HTTP transport, static and dynamic tools
builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithTools<PropertyTools>()               // Static tools via [McpServerTool]
    .WithTools(dynamicTools.ToArray());       // Dynamic tools from MySQL

// Configure OpenTelemetry
builder.Services.AddOpenTelemetry()
    .WithTracing(b => b
        .AddSource("*")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
    )
    .WithMetrics(b => b
        .AddMeter("*")
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
    )
    .WithLogging()
    .UseOtlpExporter();

builder.Logging.AddConsole();

var app = builder.Build();

// MCP endpoint at /mcp/messages/
app.MapMcp();
app.Run();
