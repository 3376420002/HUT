import uvicorn

from api import disease_date_api, paients_api
from fastapi import FastAPI
from core.config import settings

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Eye Analysis Backend is Running!"}


app.include_router(disease_date_api.router)
app.include_router(paients_api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
