from sql_tools import SQLTools
from sql_database import SQLDatabase
from llm import OpenaiLLM, chat_completion_request
from utils import format_string, format_fa
from sqlalchemy import create_engine
from tenacity import retry, wait_random_exponential, stop_after_attempt
import requests
from prompt import agent_prompt, few_shot
from action import AgentAction

server = 'uapply-prod-sql-server.database.windows.net'
user = 'uapply-prod'
password = '0HdPdWMDHyL@F*xB*xmJPDHg#01Ier@Q'
database = 'uapply-prod-sql-server-db'

from urllib.parse import quote_plus
encoded_password = quote_plus(password)
pg_uri = f"mssql+pymssql://{user}:{encoded_password}@{server}/{database}"

engine = create_engine(pg_uri)

sql_database = SQLDatabase(engine)
llm = OpenaiLLM()
tools = SQLTools(llm, sql_database)

available_functions = {'sql_db_query': tools.sql_db_query,
                       'sql_db_list_tables': tools.sql_db_list_tables,
                       'sql_db_schema': tools.sql_db_schema,
                       'sql_db_query_checker': tools.sql_db_query_checker
                       }

agent_action = AgentAction(toolkit=available_functions)

def main():
    question = "what is the basic resquirement of University of Waterloo?"

    query = agent_prompt.format(input = question, top_k=10, few_shot=few_shot)
    message = [{'role': 'user', 'content': query}]

    while True:
        response = chat_completion_request(message)
        print("***"*20)
        print("LLM response")
        print(response)
        print("***"*20)

        agent_action.parse(response)
        action_result = agent_action.run()
        if 'output' in action_result:
            return action_result['output']
        else:
            observation = action_result['observation']
            query += '\n' + response
            query += f'Observation: {observation}\n'
            print("---"*10)
            print("The next input")
            print(query)
            print("---"*10)
            message = [{'role': 'user', 'content': query}]

if __name__ == "__main__":
    answer = main()
    print(answer)