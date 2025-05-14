using System.Threading.Tasks;

namespace MyDotNetApi.Tools
{
    [FunctionTool("weather_tool", "Provides weather information for a given city.")]
    public class WeatherTool
    {
        public static async Task<string> RunAsync(string city)
        {
            // Placeholder implementation
            return await Task.FromResult($"The weather in {city} is sunny with a temperature of 25°C.");
        }
    }
}