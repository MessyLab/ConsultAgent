from abc import abstractclassmethod
import openai
import os
import time
from config import ConfigParser
from prompt import system_prompt, format_response

class LLM:
    def __init__(self) -> None:
        pass

    @abstractclassmethod
    def get_response():
        pass


