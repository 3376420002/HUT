from fastapi import Depends
from sqlalchemy.orm import Session

from db.DB import SessionLocal
from models.entity import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_userPassword(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == username).first()
    if user:
        return user.password
    else:
        return None