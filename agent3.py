from abc import abstractclassmethod
from openai import OpenAI
import os
import time
from config import ConfigParser
# from prompt import system_prompt
import json

class LLM:
    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def get_response():
        pass

class DetectAgent:
    def __init__(self, system_prompt: str):
        super(DetectAgent, self).__init__()
        self.config = ConfigParser()

        self.model = self.config.get(key='openai')['detect_model']
        self.temperature = self.config.get(key='openai')['temperature']
        self.max_tokens = 2048
        self.topp = self.config.get(key='openai')['top_p']
        self.seed = self.config.get(key='openai')['seed']
        self.client = OpenAI(api_key = self.config.get(key='openai')['api_key'])
        self.system_prompt = system_prompt

    @staticmethod
    def concat_chat_message(system_prompt, history, query):
        messages = []
        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        return messages

    def get_response(self,
                     messages,
                     stream=False,
                     timeout=10,
                     **kwargs):

        messages.insert(0, {"role": "system", "content": self.system_prompt})
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                temperature = self.temperature,
                stream = stream,
                max_tokens = self.max_tokens,
                top_p = self.topp,
                seed = self.seed,
                timeout = timeout,
            )
            
            result = response.choices[0].message.content
            json_part = result.split('```json\n')[1].split('\n```')[0]
            messages.pop(0)
            return json.loads(json_part)

        except Exception as e:
            messages.pop(0)
            print(e)

        