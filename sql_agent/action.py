from typing import Union, Dict
import re

FINAL_ANSWER_ACTION = "Final Answer:"
FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE = (
    "Parsing LLM output produced both a final answer and a parse-able action:"
)

class AgentAction:
    def __init__(self, toolkit: Dict=None):
        self.available_functions = toolkit
        self.tool = None
        self.tool_exist = True
        self.tool_input = None
        self.tool_input_exist = True
        self.final_answer = None

    def parse(self, text: str):
        includes_answer = FINAL_ANSWER_ACTION in text
        regex = (
            r"Action\s*\d*\s*:[\s]*(.*?)[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)"
        )
        action_match = re.search(regex, text, re.DOTALL) 
        if action_match:
            if includes_answer:
                print(f"{FINAL_ANSWER_AND_PARSABLE_ACTION_ERROR_MESSAGE}: {text}")
            
            self.tool = action_match.group(1).strip()
            action_input = action_match.group(2)
            tool_input = action_input.strip(" ")
            self.tool_input = tool_input.strip('"')
        
        elif includes_answer:
            self.final_answer = text.split(FINAL_ANSWER_ACTION)[-1].strip()
        
        elif not re.search(
            r"[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)", text, re.DOTALL
        ):
            self.tool_exist = False

        elif not re.search(
            r"[\s]*Action\s*\d*\s*Input\s*\d*\s*:[\s]*(.*)", text, re.DOTALL
        ):
            self.tool_input_exist = False
            

    def run(self):
        if self.final_answer != None:
            return {"output": self.final_answer}
        
        if self.tool in self.available_functions:
            if self.tool_input == '':
                result = self.available_functions[self.tool]()
                return {"observation": str(result)}
            else:
                result = self.available_functions[self.tool](self.tool_input)
                return {"observation": str(result)}
        else:
            if self.tool_exist == False:
                return {"observation": "Invalid Format: Missing 'Action:' after 'Thought:"}
            elif self.tool_input_exist == False:
                return {"observation": "Invalid Format: Missing 'Action Input:' after 'Action:'"}
            else:
                return {"observation": "The tool is not exist"}

    