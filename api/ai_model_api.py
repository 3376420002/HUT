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
        # print(i)
        # print(type(i))
        # print(i.path)
        base64_image = {
            "image": i.path,
        }
        # print(base64_image)
        try:
            contents = requests.post(url, json=base64_image)
            print(contents.status_code)
        except Exception as e:
            logging.error(e)
        if contents:
            content = contents.json()
            logging.info(content)
            print(content)
            # tag = -1
            # tag_name = ""
            # for key, value in message["main_classification"]["probabilities"].items():
            #     if value > tag:
            #         tag = value
            #         tag_name = key
            merged_probabilities = content["main_classification"]["probabilities"]
            if "糖尿病性视网膜病变" in content["main_classification"]["probabilities"] and content["main_classification"]["probabilities"]["糖尿病性视网膜病变"] > 0.5:
                tag_tng = content["main_classification"]["probabilities"].get("糖尿病性视网膜病变")
                del content["main_classification"]["probabilities"]["糖尿病性视网膜病变"]
                sum = 0
                for key2, value2 in content["sub_classification"]["probabilities"].items():
                    sum += value2
                for key2, value2 in content["sub_classification"]["probabilities"].items():
                    content["sub_classification"]["probabilities"][key2] = round((value2 / sum) * tag_tng, 3)

                merged_probabilities =content["main_classification"]["probabilities"] | content["sub_classification"]["probabilities"]

            sorted_probabilities = dict(sorted(merged_probabilities.items(), key=lambda item: item[1], reverse=True))
            probabilities = [{"name": name, "probability": probability} for name, probability in sorted_probabilities.items()]

            element = {
                "index": i.index,
                "name": i.name,
                "path": content["vessel_segmentation"]["probability_map"],
                "probabilities": probabilities,
                "enhanced_image": content["enhanced_image"]
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
    # message = {
    #     "segmentation_result": "base64编码的分割掩码图像"
    # }
    request_json = {
        "image": "base64编码的OCT图像"
    }
    response = requests.post(url, json=request_json)
    if response.status_code == 200:
        data = response.json()
        response = {
            "code": 1,
            "message": "success",
            "data": data["segmentation_result"]
        }
        return response





