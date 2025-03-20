from pydantic import BaseModel


class TokenRequest(BaseModel):
    token: str


class LoginRequest(BaseModel):
    name: str
    password: str


class DiseaseDateAge(BaseModel):
    token: str
    firstAge: int
    secondAge: int
    thirdAge: int
    forthAge: int
    fifthAge: int

