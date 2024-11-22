from typing import Dict, List

from pydantic import BaseModel


# 登陆,登陆之后会直接返回用户的个人信息
class LoginResp(BaseModel):
    stdID: str  # 学号
    place: str  # 作为
    tempQuestionNum: int  # 当前的问题序号
    totalQuestionNum: int  # 总问题数量
    countRight: int


# 通过questionID和stdID获取题目的信息(如果没作答过的话)
class GetQuestionResp(BaseModel):
    questionID: int
    content: str
    options: List[str]
    tempQuestionNum: int
    totalQuestionNum: int
    countRight: int


class GetFinishQuestionResp(BaseModel):
    # 问题表
    questionID: int
    content: str
    options: List[str]
    answer: str
    # 用户作答表
    stdID: str
    status: bool
    useTime: str
    userAnswer: str


class UploadAnswerResp(BaseModel):
    # 问题表
    questionID: int
    content: str
    options: List[str]
    answer: str
    # 用户作答表
    stdID: str
    status: bool
    useTime: str
    userAnswer: str
