using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        // Add controllers for MVC/Web API functionality
        services.AddControllers();
        
        // Register ToolService as Singleton (if ToolService is implemented properly)
        services.AddSingleton<ToolService>();
    }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
    {
        if (env.IsDevelopment())
        {
            app.UseDeveloperExceptionPage();
        }
        else
        {
            // In production, use HTTPS redirection and other middleware
            app.UseHttpsRedirection();
            app.UseHsts();
        }

        // Enable routing and map controllers
        app.UseRouting();
        app.UseEndpoints(endpoints =>
        {
            endpoints.MapControllers();
        });
    }
}
