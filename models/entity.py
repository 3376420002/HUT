from sqlalchemy import Column, Integer, String
from db.DB import Base


class Pairnts(Base):
    __tablename__ = 'pairnts'

    name = Column(String(50))
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(10))
    age = Column(Integer)
    reportId = Column(Integer)


class Paients_report(Base):
    __tablename__ = 'paients_report'

    reportId = Column(Integer, primary_key=True, index=True)
    report_times = Column(Integer)
    time = Column(String(50))
    status = Column(String(50))
    Aiadivice = Column(String(50))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    gender = Column(String(10))
    age = Column(Integer)
    department = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))


class User_password(Base):
    __tablename__ = 'user_password'

    accountId = Column(Integer, primary_key=True, index=True)
    password = Column(String(50))
