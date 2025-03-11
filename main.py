import uvicorn

from api import disease_date_api, paients_api
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
    return {"message": "Eye Analysis Backend is Running!"}


app.include_router(disease_date_api.router)
app.include_router(paients_api.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
