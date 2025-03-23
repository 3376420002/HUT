import logging
import requests

from core.config import settings
from fastapi import APIRouter
from models.template import TokenRequest, DiseaseDate
from services.jwt_depend import decode_jwt_token


router = APIRouter()


@router.post("/aibo")
async def predict(request: list[DiseaseDate]) -> dict:
    # payload = decode_jwt_token(request.token)
    # if not payload:
    #     return {
    #         "code": 0,
    #         "message": "token验证失败",
    #         "data": ""
    #     }
    url = settings.AI_MODEL_URL+"/api/fundus_analysis"
    logging.info(url)
    data = []
    for i in request:
        base64_image = i["path"]
        # request = requests.post(url,json = base64_image)
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
                "正常": 0.390
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
        },
        "enhanced_image":"base64编码的增强图像"
    }
            # tag = -1
            # tag_name = ""
            # for key, value in message["main_classification"]["probabilities"].items():
            #     if value > tag:
            #         tag = value
            #         tag_name = key
            merged_probabilities = message["main_classification"]["probabilities"]
            if "糖尿病性视网膜病变" in message["main_classification"]["probabilities"] and message["main_classification"]["probabilities"]["糖尿病性视网膜病变"] > 0.5:
                tag_tng = message["main_classification"]["probabilities"].get("糖尿病性视网膜病变")
                del message["main_classification"]["probabilities"]["糖尿病性视网膜病变"]
                sum = 0
                for key2, value2 in message["sub_classification"]["probabilities"].items():
                    sum += value2
                for key2, value2 in message["sub_classification"]["probabilities"].items():
                    message["sub_classification"]["probabilities"][key2] = round((value2 / sum) * tag_tng, 3)

                merged_probabilities =message["main_classification"]["probabilities"] | message["sub_classification"]["probabilities"]

            sorted_probabilities = dict(sorted(merged_probabilities.items(), key=lambda item: item[1], reverse=True))
            probabilities = [{"name": name, "probability": probability} for name, probability in sorted_probabilities.items()]

            element = {
                "index": i["index"],
                "name": i["name"],
                "path": message["vessel_segmentation"]["mask"],
                "probabilities": probabilities,
                "enhanced_image": message["enhanced_image"]
            }
            data.append(element)

    response = {
        "code": 1,
        "message": "success",
        "data": data
    }
    return response


@router.post("/aioct")
async def predict(request: str) -> dict:
    payload = decode_jwt_token(request.token)
    if not payload:
        return {
            "code": 0,
            "message": "token验证失败",
            "data": ""
        }
    url = settings.AI_MODEL_URL + "/api/oct_segmentation"
    # request = requests.get(url)
    message = {
        "segmentation_result": "base64编码的分割掩码图像"
    }
    request_json = {
        "image": "base64编码的OCT图像"
    }
    response = requests.post(url, json=request_json)
    if response.status_code == 200:
        data = response.json()
        response = {
            "code": 1,
            "message": "success",
            "data": message
        }
        return response





