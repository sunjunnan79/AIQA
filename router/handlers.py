from fastapi import APIRouter, Depends
from api import request, response
from service import service

router = APIRouter()


def get_service() -> service.Service:
    return service.Service()


@router.post("/login", response_model=response.LoginResp, summary="用户登录",
             description="用户通过学号登录，登录成功后返回个人信息,包括学号和座位(实际上没什么用)")
async def login(req: request.LoginReq, service: service.Service = Depends(get_service)):
    """
    用户登录接口

    Args:
        req (LoginReq): 登录请求，包括学号和座位(感觉没什么用)。

    Returns:
        LoginResp: 包含用户的学号、登录地点和问题进度信息。
    """
    return service.login(req)


@router.get(
    "/getQuestion",
    response_model=response.GetQuestionResp,
    summary="获取题目信息",
    description="通过 URL 查询参数传递 questionID 和 stdID 获取题目的信息，不包含答案,用于用户获取作答题目"
)
async def getQuestion(
        questionID: int,
        service: service.Service = Depends(get_service)
):
    """
    获取题目信息接口

    Args:
        questionID (int): 问题的唯一标识符。

    Returns:
        GetQuestionResp: 包括问题的 ID、内容和答案（可能为空）。
    """
    req = request.GetQuestionReq(questionID=questionID)
    return service.getQuestion(req)


@router.get(
    "/getFinishQuestion",
    response_model=response.GetFinishQuestionResp,
    summary="获取题目完成情况",
    description="通过 URL 查询参数传递 questionID 和 stdID 获取包含答案和用户完成情况的题目信息,用于查看用户已经完成的题目"
)
async def getFinishQuestion(
        questionID: int,
        stdID: str,
        service: service.Service = Depends(get_service)
):
    """
    获取题目完成情况接口

    Args:
        questionID (int): 问题的唯一标识符。
        stdID (str): 学号，标识具体用户。

    Returns:
        GetFinishQuestionResp: 包含问题信息、用户作答状态和使用时间。
    """
    req = request.GetFinishQuestionReq(questionID=questionID, stdID=stdID)
    return service.getFinishQuestion(req)


@router.post(
    path="/uploadAnswer",
    response_model=response.UploadAnswerResp,
    summary="提交答案",
    description="用户提交答案后返回题目信息和作答状态"
)
async def uploadAnswer(req: request.UploadAnswerReq, service: service.Service = Depends(get_service)):
    """
    提交答案接口

    Args:
        req (GiveAnswerReq): 请求参数，包括 questionID、用户学号、答案以及答题时间。

    Returns:
        GiveAnswerResp: 包含问题信息、用户答案、状态和作答时间。
    """
    return service.uploadAnswer(req)
