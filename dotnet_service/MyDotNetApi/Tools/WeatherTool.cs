using System.Threading.Tasks;

namespace MyDotNetApi.Tools
{
    [FunctionTool("weather_tool", "Returns weather information.")]
    public class WeatherTool
    {
        public static async Task<string> RunAsync(string city)
        {
            return await Task.FromResult($"The weather in {city} is sunny with a temperature of 25°C.");
        }
    }
}
