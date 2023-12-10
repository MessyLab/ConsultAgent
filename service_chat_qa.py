import streamlit as st
from st_chat_message import message
import json
from prompt import AGENT_SYSTEM_PROMPT, CONSULT_SYSTEM_PROMPT, FUNCTION_CALLING_PROMPT, CONTEXT_ANY_PROMPT
from function import function_list

from openai import OpenAI

from rdb_service import DatabaseAgent
from agent1 import OpenaiLLMwF
from agent2 import OpenaiLLM
from agent3 import DetectAgent
from qa_service import QAService



def main():
    llm = OpenAI(api_key = "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")

    db_agent = DatabaseAgent()

    Session = db_agent.init_connection_db()
    user_uuid = db_agent.create_new_user()
    print(f"**** logging information user uuid {user_uuid}")
    
    qa_svc = QAService()

    missing_fields = db_agent.check_missing_fields(user_uuid)
    print(f"**** logging information missing_fields {missing_fields}")

    available_functions = {
        "add_scores": db_agent.add_scores,
        "add_target_infor": db_agent.add_target_infor,
        # "search_answers": qa_svc.get_response
    }

    function_model = OpenaiLLMwF(FUNCTION_CALLING_PROMPT)
    chat_model = OpenaiLLM(AGENT_SYSTEM_PROMPT)
    detect_model = DetectAgent(CONTEXT_ANY_PROMPT)


    history_messages = []
    input_messages = []
    

    while True:

        print("#####"*20)
        query = input()
        print("#####"*20)
        if query:
            history_messages.append({"role":"user", "content": query})

            detect_response = detect_model.get_response(history_messages)
            print(history_messages)
            print(f"***** logging information detect response : \n {detect_response} \n")

            if len(detect_response["question"]) > 1:
                knowledge_base = qa_svc.get_responses(detect_response["question"])
                print(f"***** logging information knowledge base : \n {knowledge_base} \n")

                input_message = f"""参考知识库中的答案，简练地回答用户问题，并回到自己的人设
                                知识库内容：
                                {knowledge_base}

                                用户信息：
                                {query}
                                """
                input_messages.append({"role": "user", "content": input_message})
            
            else:
                input_messages.append({"role": "user", "content": query})


            if len(detect_response["answer"]) > 1:
                function_message = [{"role": "user", "content": detect_response["answer"]}]
                function_respond = function_model.get_response(function_message, functions=function_list)

                print(f"***** logging information function respond : \n {function_respond} \n")
                
                missing_fields = db_agent.check_missing_fields(user_uuid)
                print(f"***** logging information missing_fields :  \n {missing_fields} \n")

                function_call = function_respond.function_call

                if function_call:
                    method_name, method_args = function_call.name, function_call.arguments
                    print("-----" * 20)
                    print(f"***** logging information calling function name {method_name} and parameter {method_args}")
                    print("-----" * 20)

                    try:
                        # call function
                        method_args_dict = json.loads(method_args)
                        result = available_functions[method_name](Session, user_uuid, method_args_dict)
                    except:
                        print("***** logging information function calling error")
            
            
            print(f"***** logging information input messages {input_messages}")
            chat_respond = chat_model.get_response(input_messages)

            print(f"***** logging information chat agent respond {chat_respond}")
            print("#####"*20)
            print(chat_respond)
            print("#####"*20)

            history_messages.append({"role": "assistant", "content": chat_respond})
            input_messages = history_messages


if __name__ == "__main__":
    main()