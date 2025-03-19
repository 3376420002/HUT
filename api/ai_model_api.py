import logging
import requests

from fastapi import APIRouter
from models.template import TokenRequest


router = APIRouter()


@router.post("/aibo")
async def predict(request: TokenRequest) -> dict:
    logging.info(f"Received request: {request}")
    # request = requests.get("http://192.168.1.202:5000/api/fundus_analysi")
    # if request.status_code == 200:
    if 1 == 1:
        # 解析 JSON 数据
        message = {
    "main_classification": {
        "probabilities": {
            "其他疾病": 0.123,
            "糖尿病性视网膜病变": 0.456,
            "病理性近视": 0.234,
            "白内障": 0.345,
            "老年性黄斑部病变": 0.567,
            "青光眼": 0.678,
            "高血压视网膜病变": 0.789,
            "正常": 0.890
        }
    },
    "sub_classification": {
        "probabilities": {
            "正常": 0.123,
            "轻度": 0.234,
            "中度": 0.345,
            "重度": 0.456,
            "增值性病变": 0.567
        }
    },
    "vessel_segmentation": {
        "mask": "base64编码的分割掩码图像"
    }
}

        probabilities = message["main_classification"]["probabilities"]
        sorted_probabilities = dict(sorted(probabilities.items(), key=lambda item: item[1], reverse=True))
        data = [{"name": name, "probability": probability} for name, probability in sorted_probabilities.items()]

        response = {
            "code": 1,
            "message": "success",
            "data": data
        }
        return response

