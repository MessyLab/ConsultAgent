add_target_infor_des = """
    在用户回复了意向国家，意向大学，意向专业，留学预算或这未来求职方向任意信息之后，
    使用这个函数，将用户回复的信息添加到数据库中

    用户一次可能只给出一个参数信息，这个时候另外的参数则返回 ``
"""


function_list = [
    {
        "name": "add_scores",
        "description": "add the english score into the database, 用户可能只有一个成绩，这个时候另外一个成绩则返回 `` ",
        "parameters": {
            "type": "object",
            "properties": {
                "ielt": {
                    "type": "string",
                    "description": "the score of IELT"
                },
                "toelf": {
                    "type": "string",
                    "description": "the score of TOEFL"
                },
                "gpa": {
                    "type": "string",
                    "description": "the score of GPA"
                }
            },
            "required": ["ielt", "toelf", "gpa"]
        }
    },

    # {
    #     "name": "search_schoolprogram_by_ocp", 
    #     "description": "add the GPA score into the database",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "gpa": {
    #                 "type": "string",
    #                 "description": "the score of GPA"
    #             }
    #         },
    #         "required": ["gpa"]
    #     }
    # },

    {
        "name": "add_target_infor",
        "description": add_target_infor_des,
        "parameters": {
            "type": "object",
            "properties": {
                "trg_country" : {
                    "type": "string",
                    "description": "the intended country for user study abroad destination"
                },
                "trg_uni" : {
                    "type": "string",
                    "description": "the intended university for user study abroad destination"
                },
                "trg_major" : {
                    "type": "string",
                    "description": "the intended major for user study abroad destination"
                },
                "trg_job" : {
                    "type": "string",
                    "description": "the user's future target job after graducation"
                },
                "budget" : {
                    "type": "string",
                    "description": "the budget for study abroad"
                }
            },
            "required": ["trg_country", "trg_uni", "trg_major", "trg_job", "budget"]
        }
    },

    # {
    #     "name": "search_answers",
    #     "description": "search the answer based on user query",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "query": {
    #                 "type": "string",
    #                 "description": "the real question from user"
    #             }
    #         },
    #         "required": ["query"]
    #     }
    # },

    # {
    #     "name": "make_a_plan",
    #     "description": "在用户完成了基本信息的录入之后，根据用户输入的信息生成"
    # }

    # {
    #     "name": "add_target_university",
    #     "description": "add the target university for user study abroad destination into the database",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "trg_uni" : {
    #                 "type": "string",
    #                 "description": "the intended university for user study abroad destination"
    #             }
    #         },
    #         "required": ["trg_uni"]
    #     }
    # },

    # {
    #     "name": "add_target_major",
    #     "description": "add the target major for user study abroad destination into the database",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "trg_major" : {
    #                 "type": "string",
    #                 "description": "the intended major for user study abroad destination"
    #             }
    #         },
    #         "required": ["trg_major"]
    #     }
    # },

    # {
    #     "name": "add_target_job",
    #     "description": "add the user's future target job into the database",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "trg_job" : {
    #                 "type": "string",
    #                 "description": "the user's future target job after graducation"
    #             }
    #         },
    #         "required": ["trg_job"]
    #     }
    # }

]