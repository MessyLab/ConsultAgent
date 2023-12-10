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
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'history_messages' not in st.session_state:
        st.session_state['history_messages'] = []
    if 'input_messages' not in st.session_state:
        st.session_state['input_messages'] = []

    db_agent = DatabaseAgent()

    Session = db_agent.init_connection_db()
    # user_uuid = db_agent.create_new_user()
    # print(f"**** logging information user uuid {user_uuid}")
    if 'user_uuid' not in st.session_state:
        st.session_state['user_uuid'] = db_agent.create_new_user()
        print()
        print(st.session_state['user_uuid'])
    
    qa_svc = QAService()

    missing_fields = db_agent.check_missing_fields(st.session_state['user_uuid'])
    print(f"**** logging information missing_fields {missing_fields}")

    available_functions = {
        "add_scores": db_agent.add_scores,
        "add_target_infor": db_agent.add_target_infor,
        # "search_answers": qa_svc.get_response
    }

    function_model = OpenaiLLMwF(FUNCTION_CALLING_PROMPT)
    chat_model = OpenaiLLM(AGENT_SYSTEM_PROMPT)
    detect_model = DetectAgent(CONTEXT_ANY_PROMPT)

    

    st.title("Upply")
    query = st.chat_input("Enter your words")

    if query:
        # history_messages.append({"role":"user", "content": query})
        st.session_state['past'].append(query)

        st.session_state['history_messages'].append(
            {"role": "user", "content": query}
        )

        detect_response = detect_model.get_response(st.session_state['history_messages'])
        # print(history_messages)
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
            
            st.session_state['input_messages'].append(
                {"role": "user", "content": input_message}
            )
            # input_messages.append({"role": "user", "content": input_message})
        
        else:
            # input_messages.append({"role": "user", "content": query})
            st.session_state['input_messages'].append(
                {"role": "user", "content": query}
            )


        if len(detect_response["answer"]) > 1:
            function_respond = function_model.get_response(st.session_state['history_messages'], functions=function_list)

            print(f"***** logging information function respond : \n {function_respond} \n")
            
            missing_fields = db_agent.check_missing_fields(st.session_state['user_uuid'])
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
                    result = available_functions[method_name](Session, st.session_state['user_uuid'], method_args_dict)
                except:
                    print("***** logging information function calling error")
        
        
        print(f"***** logging information input messages {st.session_state['input_messages']}")
        chat_respond = chat_model.get_response(st.session_state['input_messages'])

        st.session_state['generated'].append(chat_respond)

        print(f"***** logging information chat agent respond {st.session_state['input_messages']}")
        print("#####"*20)
        print(chat_respond)
        print("#####"*20)

        # history_messages.append({"role": "assistant", "content": chat_respond})
        st.session_state['history_messages'].append(
            {"role": "assistant", "content": chat_respond}
        )
        st.session_state['input_messages'] = st.session_state['history_messages']

        response_container = st.container()

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))


if __name__ == "__main__":
    main()