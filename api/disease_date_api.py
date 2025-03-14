from models.entity import *
from db.DB import get_db

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session


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


@router.get('/diseaseDates/gettest')
async def disease_date(db: Session = Depends(get_db)):
    print("test")
    # 增加
    test_db = Test(name="test", age=18)
    db.add(test_db)
    db.commit()
    db.refresh(test_db)

    # 查询
    out1 = db.query(Test).filter(Test.name == "LH").first()
    print(out1.name, out1.age)

    # 更新
    out2 = db.query(Test).filter(Test.name == "牢大").first()
    out2.age = 99
    db.commit()
    db.refresh(out2)
    print(out2.name, out2.age)

    # 删除
    out3 = db.query(Test).filter(Test.name == "何向阳").first()
    db.delete(out3)
    db.commit()
    print("delete success")

    return {"message": "success"}
