using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;
using System.Reflection;

// var attributes = type.GetCustomAttributes<FunctionToolAttribute>();
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddSingleton<ToolService>();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}

app.MapControllers();

app.Run();

