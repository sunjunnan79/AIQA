import pandas as pd
from model import models


def InitQuestion(file_path: str):
    question_dao = models.QuestionDAO()
    data = pd.read_excel(file_path)
    # 处理并存储数据
    count = 0
    for _, row in data.iterrows():
        count += 1
        print(count)
        content = row["问题"]  # 假设问题列名为“问题”
        options = row["选项"].split("，")
        answer = row["答案"]
        # 调用 DAO 存储数据
        question_dao.save_question(content=content, options=options, answer=answer)


def init(file_path: str):
    # 初始化数据库
    models.InitDB()
    InitQuestion(file_path)
