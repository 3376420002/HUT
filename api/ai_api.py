import logging

from fastapi import APIRouter
from services.ai_depend import ai
from models.template import TokenRequest

router = APIRouter()


@router.post("/aiSuggestion")
async def predict(request: TokenRequest):
    try:
        logging.info("AI suggestion API called")
        ai_suggestion = await ai.call_ai_api()
        logging.info(f"Received request for AI suggestion ")
        response = {
            "code": 1,
            "message": "成功获取ai建议",
            "data": ai_suggestion
        }
        return response
    except Exception as e:
        logging.error(f"Error while processing AI suggestion request: {e}")
        return {
            "code": 0,
            "message": "服务器错误",
            "data": e
        }


@router.post("/aiQuestion")
async def answer(token:TokenRequest):
    try:
        logging.info("AI answer API called")
        ai_answer = await ai.get_ai_answer()
        return {
            "code": 1,
            "message": "成功获取ai答案",
            "data": ai_answer
        }

    except Exception as e:
        logging.error(f"Error while processing AI answer request: {e}")
        return {
            "code": 0,
            "message": "服务器错误",
            "data": e
        }
