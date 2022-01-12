from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


try:
    DB_URL = os.getenv("DB")
    engine = create_engine(DB_URL)
    SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)
    Base = declarative_base()

    print("DATABASE CONNECTED")

except Exception as e:
    print(e)
