from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from database import Base
from sqlalchemy import Column, Integer, String


class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_name = Column(String(255))
    password = Column(String(255))
    account_description = Column(String(255))
    owner_Id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="account")
