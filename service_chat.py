import streamlit as st
from st_chat_message import message
import json
from prompt import AGENT_SYSTEM_PROMPT, CONSULT_SYSTEM_PROMPT, FUNCTION_CALLING_PROMPT
from function import function_list

from rdb_service import DatabaseAgent
from agent1 import OpenaiLLMwF
from agent2 import OpenaiLLM



def main():
    # if 'generated' not in st.session_state:
    #     st.session_state['generated'] = []
    # if 'past' not in st.session_state:
    #     st.session_state['past'] = []
    # if 'messages' not in st.session_state:
    #     st.session_state['messages'] = [{
    #         'role':'system', 
    #         'content': GENERIC_SYSTEM_PROMPT,
    #         }] if GENERIC_SYSTEM_PROMPT else ""

    db_agent = DatabaseAgent()

    Session = db_agent.init_connection_db()
    user_uuid = db_agent.create_new_user()
    
    missing_fields = db_agent.check_missing_fields()
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

    function_model = OpenaiLLMwF()
    chat_model = OpenaiLLM()

    # st.title("Upply")
    # query = st.chat_input("Enter your words")
    
    chat_agent_messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    function_agent_messages = [{"role": "system", "content": FUNCTION_CALLING_PROMPT}]
    # st.session_state["messages"].append({"role": "system", "content": query})
    while True:
        query = input()
        if query:
            # st.session_state["messages"].append({"role": "user", "content": query})
            chat_agent_messages.append({"role": "user", "content": query})
            function_agent_messages.append({"role": "user", "content": query})
            # first_respond = chat_model.get_response(messages=st.session_state['messages'],
            #                                         functions=function_list)
            function_respond = function_model.get_response(messages=function_agent_messages,
                                                    functions=function_list)
            print("*****" * 20)
            print(f"logging information function respond {function_respond}")
            chat_respond = chat_model.get_response(messages=chat_agent_messages)
            print(f"logging information agent respond {chat_respond}")
            #  st.session_state['past'].append(query)
            missing_fields = db_agent.check_missing_fields()
            print(f"logging information missing_fields {missing_fields}")

            function_call = function_respond.function_call
            # print(first_respond.content)

            if function_call:
                method_name, method_args = function_call.name, function_call.arguments
                print("-----" * 20)
                print(f"calling function name {method_name} and parameter {method_args}")
                print("-----" * 20)

                try:
                    # call function
                    method_args_dict = json.loads(method_args)
                    
                    available_functions[method_name](Session, user_uuid, method_args_dict)

                    # missing_fields = db_agent.check_missing_fields()
#                     if len(missing_fields) <= 1:
#                         information = db_agent.get_all_infor()
#                         # print(information)
#                         user_prompt = f"""
# 英语成绩：雅思：{information.eng_ielts}， 托福：{information.eng_toelf}
# GPA：{information.score_gpa}
# 意向国家：{information.target_country}
# 意向学校：{information.target_university}
# 意向专业：{information.target_major}
# 留学预算：{information.budget}
# 未来工作意向：{information.target_job}
#                         """
#                         print(user_prompt)

                except:
                    pass
                    
                # else:
                    # format_prompt = 
                    # st.session_state['messages'].append(
                    #     {"role": "user", "content": method_result}
                    # )

                    # second_response = chat_model.get_response(messages=st.session_state['messages'])
                    # second_response = chat_model.get_response(messages=chat_messages)
                    # print(first_respond.content)
                    # chat_messages.append({"role": "assistant", "content": first_respond.content})
                    # st.session_state['generated'].append(second_response.content)
                    # st.session_state['messages'].append(
                    #     {"role": "assistant", "content": second_response.get('content')}
                    # )
            
            print("*****" * 20)
            content = chat_respond.content
            # st.session_state['generated'].append(content)
            # st.session_state['messages'].append(
            #     {"role": "assistant", "content": content}
            # )
            print(content)
            # chat_messages.append({"role": "assistant", "content": content})
            chat_agent_messages.append({"role": "assistant", "content": content})
            function_agent_messages.append({"role": "assistant", "content": content})

    # response_container = st.container()

    # if st.session_state['generated']:
    #     with response_container:
    #         for i in range(len(st.session_state['generated'])):
    #             message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
    #             message(st.session_state["generated"][i], key=str(i))

if __name__ == "__main__":
    main()