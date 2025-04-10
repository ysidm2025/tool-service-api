using System.ComponentModel;

[Description(@"
    Fetches weather information for a given city.
")]
public class WeatherTool : Tool
{
    public override string Run(string city, string units)
    {
        return $"Weather in {city} is 15°C with units {units}";
    }
}
