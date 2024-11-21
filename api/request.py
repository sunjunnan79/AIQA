from pydantic import BaseModel


# 登陆,登陆之后会直接返回用户的个人信息
class LoginReq(BaseModel):
    stdID: str
    place: str  # 我也不知道有什么意义的字段,真不如password


# 通过questionID和stdID获取题目的信息,只有题目没有答案
class GetQuestionReq(BaseModel):
    questionID: int
    stdID: str


# 通过questionID和stdID获取题目的信息,有答案和题目的作答情况信息
class GetFinishQuestionReq(BaseModel):
    questionID: int
    stdID: str


class UploadAnswerReq(BaseModel):
    questionID: int
    # 用户作答表
    stdID: str
    start: str
    end: str
    userAnswer: str
