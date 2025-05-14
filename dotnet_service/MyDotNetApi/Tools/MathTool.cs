using System.Threading.Tasks;

namespace MyDotNetApi.Tools
{
    [FunctionTool("math_tool", "Performs arithmetic operations.")]
    public class MathTool
    {
        public static async Task<string> RunAsync(double a, double b, string operation)
        {
            double result = operation switch
            {
                "add" => a + b,
                "subtract" => a - b,
                "multiply" => a * b,
                "divide" => b != 0 ? a / b : throw new ArgumentException("Cannot divide by zero."),
                _ => throw new ArgumentException("Invalid operation.")
            };

            return await Task.FromResult($"Result: {result}");
        }
    }
}
