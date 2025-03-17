import uvicorn

from api import disease_date_api, paients_api, ai_api
from fastapi import FastAPI
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    print("Hello")
    return {"message": "根据患者的信息，以下是您可以提供的诊断建议和治疗流程：\n\n###1. 治疗建议：\n由于患者已经处于糖尿病晚期阶段，治疗重点应该包括控制血糖水平、管理并发症、调整生活方式及饮食习惯。建议进行个性化的治疗方案，以达到控制病情、延缓病情进展的目的。\n\n###2. 检查计划：\na. 定期检测血糖水平，包括空腹血糖、餐后血糖和糖化血红蛋白（HbA1c）。\nb. 定期检查眼底情况，以排除糖尿病视网膜病变。\nc. 定期检查肾功能，包括肾功能指标、微量蛋白尿。\nd. 定期检查神经系统情况，以排除糖尿病周围神经病变。\n\n###3. 用药建议：\n根据病情严重程度和患者个体情况，可能需要进行药物治疗。常用的药物包括口服降糖药物、胰岛素等，具体的药物选择应根据患者的全面评估和监测情况来确定，以确保治疗效果和安全性。\n\n请注意，以上建议仅供参考，具体的诊断和治疗方案应由专业医生根据临床情况综合判断。如有需要，请尽快将患者转诊给专科医生进行进一步评估和治疗。"}


app.include_router(disease_date_api.router)
app.include_router(paients_api.router)
app.include_router(ai_api.router)



if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
