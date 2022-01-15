from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_verified = Column(Boolean(create_constraint=False), default=False)

    account = relationship("Account", back_populates="owner")
    verification_code = relationship("VerificationCode", back_populates="owner")


class VerificationCode(Base):

    __tablename__ = "verification_code"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(Integer)
    owner_Id = Column(Integer, ForeignKey("user.id"))
    expiry = Column(DateTime)

    owner = relationship("User", back_populates="verification_code")
