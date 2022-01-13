from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_verified = Column(Boolean(create_constraint=False), default=False)

    account = relationship("Account", back_populates="owner")
