import random
from time import time, timezone
import User.user_model as user_model
from sqlalchemy.orm import Session
from fastapi.params import Depends
from fastapi import HTTPException, status
from Dto import account_dto, user_dto
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from typing import Optional
from dateutil import parser
import database

load_dotenv()
get_db = database.get_db


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
    return generate_jwt(new_user)


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


def generate_jwt(body: OAuth2PasswordRequestForm = Depends()):

    expire = datetime.now(timezone.utc).astimezone() + timedelta(minutes=15)

    jwt_payload = {"email": body.email, "id": body.id, "expiration": str(expire)}

    return jwt.encode(jwt_payload, os.getenv("secretKey"), algorithm="HS256")


def validate_jwt(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="token")),
    db: Session = Depends(get_db),
):
    removeQuotes = token.replace('"', "")
    try:
        jwt_payload = jwt.decode(
            removeQuotes, os.getenv("secretKey"), algorithms="HS256"
        )

        return check_payload(jwt_payload, db)

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_payload(jwt_payload, db: Session):

    user = (
        db.query(user_model.User)
        .filter(
            user_model.User.id == jwt_payload["id"],
            user_model.User.email == jwt_payload["email"],
        )
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"error": "User doesn't exist"},
        )
    return user


def generate_code(user: user_model.User, db: Session):
    code_table = user_model.VerificationCode

    check_code_exist(user, db)

    db.query(code_table).filter(code_table.owner_Id == user.id).delete()

    db.commit()
    new_code = code_table(
        code=int(random.randint(100000, 999999)),
        owner_Id=user.id,
        expiry=datetime.now() + timedelta(minutes=5),
    )
    db.add(new_code)
    db.commit()
    db.refresh(new_code)

    return new_code


def check_code_exist(user: user_model.User, db: Session):
    code_table = user_model.VerificationCode
    code = db.query(code_table).filter(code_table.owner_Id == user.id).first()

    if code is not None:
        if code.expiry >= datetime.now():

            raise HTTPException(
                status_code=403,
                detail="Code already sent to the email",
                headers={"error": "Code is still valid"},
            )

    return None


def verify_code(code: int, user: user_model.User, db: Session):
    code_table = user_model.VerificationCode
    user_table = user_model.User
    check_code = (
        db.query(code_table)
        .filter(code_table.code == code, code_table.owner_Id == user.id)
        .first()
    )

    check_code_error(check_code)

    db.query(code_table).filter(code_table.owner_Id == user.id).delete()
    user.is_verified = True
    db.commit()

    return {"msg", "Successfully Verified"}


def check_code_error(code: user_model.VerificationCode):
    if code is None:
        raise HTTPException(
            status_code=403,
            detail="Wrong Code",
            headers={"error": "Wrong Code"},
        )

    if code.expiry < datetime.now():
        raise HTTPException(
            status_code=403,
            detail="Code Expired",
            headers={"error": "Code Expired"},
        )
