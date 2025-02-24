from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class TokenRequest(BaseModel):
    token: str


class DiseaseDate(BaseModel):
    token: str
    firstAge: int
    secondAge: int
    thirdAge: int
    fourthAge: int
    fifthAge: int


@router.post('/diseaseDates/getDiseasesDistributio')
async def disease_date(request: TokenRequest):
    return {"token": request.token}


@router.post('/diseaseDates/getDiseaseConditionByAge')
async def disease_date(request: DiseaseDate):
    return {
        "token": request.token,
        "firstAge": request.firstAge,
        "secondAge": request.secondAge,
        "thirdAge": request.thirdAge,
        "fourthAge": request.fourthAge,
        "fifthAge": request.fifthAge
    }


@router.post('/diseaseDates/getPaientsNum')
async def disease_date(request: TokenRequest):
    return {"token": request.token}