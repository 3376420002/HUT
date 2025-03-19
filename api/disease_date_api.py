import logging

from db.DB import get_db
from models.entity import *
from fastapi import APIRouter, Depends
from models.template import TokenRequest, DiseaseDateAge
from sqlalchemy.orm import Session

router = APIRouter()


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


@router.post('/diseaseDates/getDiseasesDistribution')
async def disease_dirtribution(db: Session = Depends(get_db)) -> dict:
    try:
        result = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        outcomes = db.query(Paients.outCome).all()
        for outcome in outcomes:
            if outcome[0]:
                print(outcome[0])
                if outcome[0] >= 10:
                    result[1] += 1
                else:
                    result[outcome[0]] += 1

        data = {
            "diabetes": result[1],
            "glaucoma": result[2],
            "cataract": result[3],
            "AMD": result[4],
            "hypertension": result[5],
            "myopia": result[6],
            "others": result[7]
        }

        response = {
            "code": 1,
            "message": "成功获取数据",
            "data": data
        }
        logging.info(response)
    except Exception as e:
        response = {
            "code": 0,
            "message": "获取数据失败",
            "data": str(e)
        }
        logging.error("Error:获取疾病分布失败", response)
    return response


@router.post('/diseaseDates/getDiseaseDate')
async def disease_date(request: DiseaseDateAge, db: Session = Depends(get_db)) -> dict:
    try:
        print(request.token)
        result = [[0 for _ in range(9)] for _ in range(7)]

        outcomes = db.query(Paients.outCome, Paients.age).all()
        for outcome in outcomes:
            if outcome[0]:
                if outcome[0] >= 10:
                    if outcome[1] <= request.fifthAge:
                        result[1][1] += 1
                    elif outcome[1] > request.fifthAge and outcome[1] <= request.secondAge:
                        result[1][2] += 1
                    elif outcome[1] > request.secondAge and outcome[1] <= request.thirdAge:
                        result[1][3] += 1
                    elif outcome[1] > request.thirdAge and outcome[1] <= request.forthAge:
                        result[1][4] += 1
                    elif outcome[1] > request.forthAge and outcome[1] <= request.fifthAge:
                        result[1][5] += 1
                    elif outcome[1] > request.fifthAge:
                        result[1][6] += 1
                else:
                    if outcome[1] <= request.fifthAge:
                        result[outcome[outcome[0]]][1] += 1
                    elif outcome[1] > request.fifthAge and outcome[1] <= request.secondAge:
                        result[outcome[outcome[0]]][2] += 1
                    elif outcome[1] > request.secondAge and outcome[1] <= request.thirdAge:
                        result[outcome[outcome[0]]][3] += 1
                    elif outcome[1] > request.thirdAge and outcome[1] <= request.forthAge:
                        result[outcome[outcome[0]]][4] += 1
                    elif outcome[1] > request.forthAge and outcome[1] <= request.fifthAge:
                        result[outcome[outcome[0]]][5] += 1
                    elif outcome[1] > request.fifthAge:
                        result[outcome[outcome[0]]][6] += 1



        response = {
            "code": 1,
            "message": "成功获取数据",
            "data": ""
        }
        logging.info(response)
    except Exception as e:
        response = {
            "code": 0,
            "message": "获取数据失败",
            "data": str(e)
        }
        logging.error("Error:获取疾病分布失败", response)
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
