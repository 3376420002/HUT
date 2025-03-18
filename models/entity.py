from sqlalchemy import Column, Integer, String, Text
from db.DB import Base


class Paients(Base):
    __tablename__ = 'paients'

    name = Column(String(20))
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(5))
    age = Column(Integer)
    time = Column(String(50))
    reportId = Column(String(50))
    leftphoto = Column(Text)
    rightphoto = Column(Text)
    outcom = Column(String(50))


# class Paients_report(Base):
#     __tablename__ = 'paients_report'
#
#     reportId = Column(Integer, primary_key=True, index=True)
#     time = Column(String(50))
#     status = Column(String(50))
#     photo = Column(String)
#     Aiadivice = Column(String(50))


class User(Base):
    __tablename__ = 'user'

    name = Column(String(20))
    accountId = Column(Integer, primary_key=True, index=True)
    gender = Column(String(5))
    age = Column(Integer)
    department = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    password = Column(String(50))
    photo = Column(Text)


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
