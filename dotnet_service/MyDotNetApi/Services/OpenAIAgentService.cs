using dotenv.net;
using OpenAI;
using OpenAI.Assistants;
using OpenAI.Threads;
using OpenAI.Threads.Messages;
using OpenAI.Threads.Runs;
using System.Text.Json;

namespace MyDotNetApi.Services
{
    public class OpenAIAgentService
    {
        private readonly OpenAIClient _client;
        private readonly string _assistantId;

        public OpenAIAgentService()
        {
            DotEnv.Load();
            var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY");
            _assistantId = Environment.GetEnvironmentVariable("OPENAI_ASSISTANT_ID");
            _client = new OpenAIClient(apiKey);
        }

        public async Task<string> AskAgentAsync(string query)
        {
            var thread = await _client.Threads.CreateThreadAsync();
            await _client.Threads.Messages.CreateMessageAsync(thread.Id, MessageRole.User, query);
            var run = await _client.Threads.Runs.CreateRunAsync(thread.Id, new CreateRunRequest(_assistantId));

            while (true)
            {
                var status = await _client.Threads.Runs.RetrieveRunAsync(thread.Id, run.Id);

                if (status.Status == "completed")
                    break;

                await Task.Delay(1000);
            }
                Console.WriteLine($"API Key: {apiKey}");
                Console.WriteLine($"Assistant ID: {_assistantId}");
            var messages = await _client.Threads.Messages.ListMessagesAsync(thread.Id);
            var assistantReply = messages.Data.FirstOrDefault(m => m.Role == MessageRole.Assistant);

            return assistantReply?.Content.FirstOrDefault()?.Text ?? "No response.";
        }
    }
}
