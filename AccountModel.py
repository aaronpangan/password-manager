from db import Base
from sqlalchemy import Column, Integer, String


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    accountName = Column(String(255))
    password = Column(String(255))
    accountDescription = Column(String(255))
