from fastapi import status
from fastapi.params import Depends
from fastapi.routing import APIRouter
from typing import Optional
from Dto import user_dto
from sqlalchemy.orm import Session
import database
from . import user_service
from fastapi.security import OAuth2PasswordBearer


get_db = database.get_db

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return user_service.find_user(id, db)


@router.post("")
def create_user(body: user_dto.CreateUser, db: Session = Depends(get_db)):
    return user_service.register(body, db)


@router.post("/login")
def login(body: user_dto.CreateUser, db: Session = Depends(get_db)):
    return user_service.login(body, db)


@router.post("/checktoken")
def check_token(user=Depends(user_service.validate_jwt)):
    return user


@router.post("/generate-code")
def generate_code(
    user=Depends(user_service.validate_jwt), db: Session = Depends(get_db)
):
    return user_service.generate_code(user, db)


@router.post("/verify_token/{code}")
def verify_token(
    code: int, user=Depends(user_service.validate_jwt), db: Session = Depends(get_db)
):
    return user_service.verify_code(code, user, db)
