import json

from model import models
from api import request, response


class Service:
    def __init__(self):
        # 创建 ChatOpenAI 模型
        self.userDAO = models.UserDAO()
        self.answerDAO = models.AnswerDAO()
        self.questionDAO = models.QuestionDAO()

    def login(self, req: request.LoginReq) -> response.LoginResp:
        # 用户个人信息
        user = self.userDAO.first_or_create(req.stdID, req.place)
        # 当前答题情况
        tempQuestionNum = self.answerDAO.find_latest(req.stdID)

        # 题目总数
        totalQuestionNum = self.questionDAO.get_total()
        countRight = self.answerDAO.countRight(req.stdID)
        return response.LoginResp(stdID=user.stdID, place=user.place, tempQuestionNum=tempQuestionNum,
                                  totalQuestionNum=totalQuestionNum,countRight=countRight)

    def getFinishQuestion(self, req: request.GetFinishQuestionReq) -> response.GetFinishQuestionResp:
        question = self.questionDAO.find_question(question_id=req.questionID)
        # 如果是小于这个问题id的话,说明用户没有权限查看这个题目答案
        if self.answerDAO.find_latest(req.stdID) < req.questionID:
            return response.GetFinishQuestionResp(  # 问题表
                questionID=question.id,
                content=question.content,
                options=json.loads(question.options),
                answer="",
                # 用户作答表
                stdID=req.stdID,
                status=False,
                useTime="",
                userAnswer="",

            )

        answer = self.answerDAO.find(questionID=req.questionID, stdID=req.stdID)

        useTime = self.answerDAO.calculate_time_spent_str(answer_id=answer.id)
        return response.GetFinishQuestionResp(
            # 问题表
            questionID=question.id,
            content=question.content,
            options=json.loads(question.options),
            answer=question.answer,
            # 用户作答表
            stdID=answer.stdID,
            status=answer.status,
            useTime=useTime,
            userAnswer=answer.answer,
        )

    def getQuestion(self, req: request.GetQuestionReq) -> response.GetQuestionResp:
        # 题目总数
        totalQuestionNum = self.questionDAO.get_total()
        tempQuestionNum = self.answerDAO.find_latest(req.stdID)
        countRight = self.answerDAO.countRight(req.stdID)
        question = self.questionDAO.find_question(question_id=req.questionID)

        return response.GetQuestionResp(
            # 问题表
            tempQuestionNum=tempQuestionNum,
            totalQuestionNum=totalQuestionNum,
            countRight=countRight,
            questionID=question.id,
            content=question.content,
            options=json.loads(question.options),
        )

    def uploadAnswer(self, req: request.UploadAnswerReq) -> response.UploadAnswerResp:
        question = self.questionDAO.find_question(question_id=req.questionID)
        answer = self.answerDAO.first_or_create(
            questionID=req.questionID,
            stdID=req.stdID,
            status=(question.answer == req.userAnswer),  # 这里直接判断答案正确性
            answer=req.userAnswer,
            start=req.start,
            end=req.end
        )

        useTime = self.answerDAO.calculate_time_spent_str(answer_id=answer.id)

        return response.UploadAnswerResp(
            # 问题表
            questionID=question.id,
            content=question.content,
            options=json.loads(question.options),
            answer=question.answer,
            # 用户作答表
            stdID=answer.stdID,
            status=answer.status,
            useTime=useTime,
            userAnswer=answer.answer,
        )
