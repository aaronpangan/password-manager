from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


try:
    DB_URL = os.getenv("DB")
    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    print("DATABASE CONNECTED")
except Exception as e:
    print(e)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
