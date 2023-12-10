import g4f
import json

class QAService:
    def __init__(self):
        super(QAService, self).__init__()
        self.providers = [
            g4f.Provider.Bing,
            # g4f.Provider.Hashnode,
            g4f.Provider.You,
            g4f.Provider.GeekGpt,
            # g4f.Provider.Raycast,
            # g4f.Provider.GPTalk,
            g4f.Provider.GptForLove,
            # g4f.Provider.HuggingChat,
            # g4f.Provider.DeepInfra,
            # g4f.Provider.Llama2
        ]

    def get_response(self, query, provider: g4f.Provider.BaseProvider):
        # query_prompt = """The response must be in ```json``` JSON format. 
        #                 The detail format of JSON is belowing:
        #                 ```json
        #                 {
        #                     Answer: 
        #                 }
        #                 ```
        #                 The keyword of JSON is Answer
        #                 Put all the answer into the Answer without any link
        #                 The result for 'Answer' must be a single string without line breaks. Use \n to represent new lines within the string, ensuring it can be successfully loaded by `json.loads`.
        #                 """

        # user_query = f"User question: {query}"

        # user_query += query_prompt

        response = g4f.ChatCompletion.create(
            model = g4f.models.default,
            messages=[{"role": "user", "content": query}],
            provider=provider
        )
        print(f"{provider.__name__}:", response)
        # json_part = response.split('```json\n')[1].split('\n```')[0]
        # result = json.loads(json_part)
        # return result["answer"]
        return response

    def get_responses(self, query):
        knowledge_base = ""

        for idx, provider in enumerate(self.providers):
            try:
                answer = self.get_response(query, provider)
                knowledge_base += f"reference {idx + 1}\n: {answer}\n"
            except:
                print(f"{provider.__name__} not work")

        return knowledge_base
