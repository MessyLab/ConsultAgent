from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests

class OpenaiLLM:
    def __init__(self):
        super(OpenaiLLM, self).__init__()

        self.model = "gpt-4-1106-preview"
        self.temperature = 1.0
        self.max_tokens = 2048
        self.topp = 1.0
        self.seed = 12345
        self.client = OpenAI(api_key = "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")

    @staticmethod
    def concat_chat_message(system_prompt, history, query):
        messages = []
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        return messages
    
    def get_response(self, query):
        message = [{"role":"user", "content": query}]
        response = self.client.chat.completions.create(
                    model = self.model,
                    messages = message,
                    temperature = self.temperature,
                    max_tokens = self.max_tokens,
                    top_p = self.topp,
                    seed = self.seed,
                    timeout = 10,
                )
        return response.choices[0].message.content
    
model = "gpt-4-1106-preview"
# model = "gpt-3.5-turbo-1106"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=model, stop=["\nObservation:", "\n\tObservation:"]):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + "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",
    }

    json_data = {"model": model, "messages": messages, "stop": stop}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e