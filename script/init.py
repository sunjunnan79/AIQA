import pandas as pd

# 导入你的 DAO 和模型
from model import models  # 替换为实际路径


# 定义选项转换函数
def format_options(option_str):
    options = option_str.split("，")  # 假设选项用中文逗号分隔
    formatted = {chr(65 + i): opt.strip() for i, opt in enumerate(options)}  # A, B, C, D...
    return formatted


def format_answer(options: dict, answer: str) -> str:
    """
    根据选项值找到对应的选项字母（键）。
    :param options: 字典形式的选项，如 {"A": "故意杀人", "B": "单位行贿"}
    :param answer: 需要匹配的答案内容
    :return: 对应选项的字母（键），如 "A"，若未找到则返回空字符串
    """
    for key, value in options.items():
        if value == answer:
            return key
    return ""


def InitQuestion(file_path: str):
    question_dao = models.QuestionDAO()
    data = pd.read_excel(file_path)
    # 处理并存储数据
    count=0
    for _, row in data.iterrows():
        count += 1
        print(count)
        content = row["问题"]  # 假设问题列名为“问题”
        options = format_options(row["选项"])  # 假设选项列名为“选项”
        answer = format_answer(options, row["答案"])  # 假设答案列名为“答案”

        # 调用 DAO 存储数据
        question_dao.save_question(content=content, options=options, answer=answer)

def init(file_path: str):
    # 初始化数据库
    models.InitDB()
    InitQuestion(file_path)
