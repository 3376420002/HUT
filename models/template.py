from pydantic import BaseModel


class TokenRequest(BaseModel):
    token: str


class DiseaseDate(BaseModel):
    token: str
    firstAge: int
    secondAge: int
    thirdAge: int
    fourthAge: int
    fifthAge: int
