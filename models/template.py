from pydantic import BaseModel


class TokenRequest(BaseModel):
    token: str


class DiseaseDateAge(BaseModel):
    token: str
    firstAge: int
    secondAge: int
    thirdAge: int
    forthAge: int
    fifthAge: int

