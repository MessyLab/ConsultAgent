import streamlit as st
from st_chat_message import message
import json
from prompt import AGENT_SYSTEM_PROMPT, CONSULT_SYSTEM_PROMPT, FUNCTION_CALLING_PROMPT
from function import function_list

from rdb_service import DatabaseAgent
from agent1 import OpenaiLLMwF
from agent2 import OpenaiLLM


def main():
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    if 'chat_agent_messages' not in st.session_state:
        st.session_state['chat_agent_messages'] = [{
            'role':'system', 
            'content': AGENT_SYSTEM_PROMPT,
            }] if AGENT_SYSTEM_PROMPT else ""
    if 'function_agent_messages' not in st.session_state:
        st.session_state['function_agent_messages'] = [{
            'role':'system', 
            'content': FUNCTION_CALLING_PROMPT,
            }] if FUNCTION_CALLING_PROMPT else ""

    db_agent = DatabaseAgent()

    Session = db_agent.init_connection_db()

    if 'user_uuid' not in st.session_state:
        st.session_state['user_uuid'] = db_agent.create_new_user()
        print()
        print(st.session_state['user_uuid'])
    
    missing_fields = db_agent.check_missing_fields(st.session_state['user_uuid'])
    print(f"**** logging information missing_fields {missing_fields}")

    available_functions = {
        # "add_eng": db_agent.add_eng,
        # "add_gpa": db_agent.add_gpa,
        # "add_target_country": db_agent.add_target_country,
        # "add_target_university": db_agent.add_target_university,
        # "add_target_major": db_agent.add_target_major,
        # "add_target_job": db_agent.add_target_job
        "add_scores": db_agent.add_scores,
        "add_target_infor": db_agent.add_target_infor
    }

    function_model = OpenaiLLMwF(FUNCTION_CALLING_PROMPT)
    chat_model = OpenaiLLM(AGENT_SYSTEM_PROMPT)

    st.title("Upply")
    query = st.chat_input("Enter your words")

    # chat_agent_messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    # function_agent_messages = [{"role": "system", "content": FUNCTION_CALLING_PROMPT}]


    if query:
        # chat_agent_messages.append({"role": "user", "content": query})
        # function_agent_messages.append({"role": "user", "content": query})
        st.session_state['chat_agent_messages'].append(
                {"role": "user", "content": query}
            )
        st.session_state['function_agent_messages'].append(
                {"role": "user", "content": query}
            )

        function_respond = function_model.get_response(messages=st.session_state['function_agent_messages'],
                                                    functions=function_list)
        print("*****" * 20)
        print(f"logging information function respond {function_respond}")
        chat_respond = chat_model.get_response(messages=st.session_state['chat_agent_messages'])
        print(f"logging information agent respond {chat_respond}")
        st.session_state['past'].append(query)
        missing_fields = db_agent.check_missing_fields(st.session_state['user_uuid'])
        print(f"logging information missing_fields {missing_fields}")

        function_call = function_respond.function_call

        if function_call:
            method_name, method_args = function_call.name, function_call.arguments
            print("-----" * 20)
            print(f"calling function name {method_name} and parameter {method_args}")
            print("-----" * 20)

            try:
                # call function
                method_args_dict = json.loads(method_args)
                
                available_functions[method_name](Session, st.session_state['user_uuid'], method_args_dict)
            
            except:
                    pass
            
        print("*****" * 20)
        # content = chat_respond.content
        content = chat_respond
        st.session_state['generated'].append(chat_respond)
        print(content)

        st.session_state['chat_agent_messages'].append({"role": "assistant", "content": content})
        st.session_state['function_agent_messages'].append({"role": "assistant", "content": content})

        response_container = st.container()

        if st.session_state['generated']:
            with response_container:
                for i in range(len(st.session_state['generated'])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
                    message(st.session_state["generated"][i], key=str(i))

if __name__ == "__main__":
    main()