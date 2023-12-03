from prompt import AGENT_SYSTEM_PROMPT, CONSULT_SYSTEM_PROMPT, FUNCTION_CALLING_PROMPT
from connect_db import DatabaseAgent
from agent2 import OpenaiLLM

def save_to_txt(string_content, filename='test.md'):
    with open(filename, "w", encoding='utf-8') as file:
        file.write(string_content)


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
    chat_model = OpenaiLLM()
    chat_model.model = "gpt-4-1106-preview"
    # chat_model.model = "gpt-3.5-turbo-1106"
    # chat_model.model = "gpt-4-0613"
    chat_model.max_tokens = 2048

    Session = db_agent.init_connection_db()
    # user_uuid = "c9deab9e-f812-4014-b648-976c9b4fa21e"
    user_uuid = "11ccadc9-06e5-4b9f-8384-3b5624e9a2ee"

    db_agent.user_uuid = user_uuid
    missing_fields = db_agent.check_missing_fields(user_uuid=user_uuid)
    print(missing_fields)

    if len(missing_fields) <= 1:
        information = db_agent.get_all_infor(user_uuid)
        # print(dir(information))
        # print(information)
        user_prompt = f"""
            托福 {information.eng_toelf}, GPA {information.score_gpa}，意向国家{information.target_country}，意向学校{information.target_university}，意向专业{information.target_major}，留学预算{information.budget}，未来工作意向{information.target_job}, 按照保底（Safety）、目标（Target）、冲刺（Reach）3个策略进行推荐
        """
        print(user_prompt)
        # input_prompt = CONSULT_SYSTEM_PROMPT + '\n用户资料:' + user_prompt

        plan_message = [{"role": "system", "content": CONSULT_SYSTEM_PROMPT}]
        plan_message = [{"role": "user", "content": user_prompt}]

        plan = chat_model.get_response(messages=plan_message, timeout=240)
        print(plan.content)
        save_to_txt(plan.content)
    else:
        print("test")

if __name__ == "__main__":
    main()