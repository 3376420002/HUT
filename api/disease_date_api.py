import logging

from db.DB import get_db
from models.entity import *
from fastapi import APIRouter, Depends
from models.template import TokenRequest, DiseaseDate
from sqlalchemy.orm import Session

router = APIRouter()


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
async def disease_date(db: Session = Depends(get_db)) -> dict:
    try:
        result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        mouth_data = db.query(Paients.time).all()
        for data in mouth_data:
            if data[0]:
                # mouth_time = data[0].sqlit(".")[1]
                mouth_time = data[0]

                result[int(mouth_time.split(".")[1])-1] += 1

        response = {
            "code": 1,
            "message": "成功获取数据",
            "data": result
        }
        logging.info(response)
    except Exception as e:
        response = {
            "code": 0,
            "message": "获取数据失败",
            "data": str(e)
        }
        logging.error("Error:获取月份患病人数失败",response)
    return response


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
