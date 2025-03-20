from fastapi import APIRouter
from pydantic import BaseModel
from services.jwt_depend import decode_jwt_token

router = APIRouter()


class TokenRequest(BaseModel):
    token: str


class ModifyPersonInfo(BaseModel):
    token: str
    name: str
    accountId: str
    gender: str
    age: int
    deparment: str
    email: str
    phone: str


@router.post('/patients/getPersonallnform')
async def get_person_all_info(request: TokenRequest):
    token = request.token
    print(token)
    return {"message": "success"}


@router.post('/patients/setPersonallnform')
async def set_person_info(request: ModifyPersonInfo):
    token = request.token
    name = request.name
    accountId = request.accountId
    gender = request.gender
    age = request.age
    deparment = request.deparment
    email = request.email
    phone = request.phone
    print(token, name, accountId, gender, age, deparment, email, phone)
    return {"message": "success"}
