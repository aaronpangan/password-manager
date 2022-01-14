from time import timezone
import User.user_model as user_model
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi import HTTPException
from Dto import account_dto, user_dto
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import jwt
import os
from dotenv import load_dotenv
from typing import Optional
from dateutil import parser

load_dotenv()


def find_user(id: int, db: Session):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"error": "User ID doesn't exist"},
        )
    return user


def register(body: user_dto.CreateUser, db: Session):
    user = check_by_email(body.email, db)

    if user is not None:
        raise HTTPException(
            status_code=404,
            detail="Email already Exist",
            headers={"error": "Email already Exist"},
        )

    hash_password = generate_hash(body.password)

    new_user = user_model.User(email=body.email, password=hash_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return hash_password


def login(body: user_dto.CreateUser, db: Session):

    user = check_by_email(body.email, db)

    if not user or not verify_hash(body.password, user.password):
        raise HTTPException(
            status_code=404,
            detail="User not Found",
            headers={"error": "User not Found"},
        )
    return generate_jwt(user)


def check_by_email(email: str, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()

    return user


def generate_hash(password):
    return bcrypt.using(rounds=13).hash(password)


def verify_hash(password, hashed_password):
    return bcrypt.verify(password, hashed_password)


def generate_jwt(
    body: OAuth2PasswordRequestForm = Depends(), expires: Optional[timedelta] = None
):

    expire = datetime.now(timezone.utc).astimezone() + timedelta(minutes=15)

    jwt_payload = {"email": body.email, "id": body.id, "expiration": str(expire)}

    return jwt.encode(jwt_payload, os.getenv("secretKey"), algorithm="HS256")


def validate_jwt(token: str):

    removeQuotes = token.split('"')[1]
    jwt_payload = jwt.decode(removeQuotes, os.getenv("secretKey"), algorithms="HS256")

    print(
        parser.parse(jwt_payload["expiration"])
        - datetime.now(timezone.utc).astimezone()
    )
    return jwt_payload
