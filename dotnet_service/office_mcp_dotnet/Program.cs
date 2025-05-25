using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Metrics;
using PropertyMcpServer.Tools;
using OpenTelemetry.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Register MCP server with HTTP transport and PropertyTools
builder.Services.AddMcpServer()
    .WithHttpTransport()
    .WithTools<PropertyTools>();

// Configure OpenTelemetry (logging, tracing, metrics, OTLP exporter)
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
    .WithLogging()         // Requires using OpenTelemetry;
    .UseOtlpExporter();    // Also requires using OpenTelemetry;

builder.Logging.AddConsole();

var app = builder.Build();

// Expose MCP endpoint at /mcp/messages/
app.MapMcp();

app.Run();
