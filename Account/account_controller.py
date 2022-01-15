from fastapi import status
from fastapi.params import Depends
from fastapi.routing import APIRouter
from typing import Optional
from uuid import uuid4
from Dto import account_dto
from sqlalchemy.orm import Session
import database
from . import account_service
from User import user_service


get_db = database.get_db

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("")
async def get_accounts(
    searchName: Optional[str] = None,
    user=Depends(user_service.validate_jwt),
    db: Session = Depends(get_db),
):
    return account_service.get_accounts(searchName, db, user)


@router.get("/{id}")
async def get_account(
    id: int, user=Depends(user_service.validate_jwt), db: Session = Depends(get_db)
):
    account = account_service.check_account(id, db, user)

    return account


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_account(
    body: account_dto.CreateAccount,
    user=Depends(user_service.validate_jwt),
    db: Session = Depends(get_db),
):

    return account_service.create_account(body, db, user)


@router.put("/{id}")
async def update_account(
    id: int,
    body: account_dto.CreateAccount,
    user=Depends(user_service.validate_jwt),
    db: Session = Depends(get_db),
):
    return account_service.update_account(id, body, db, user)


@router.delete("/{id}")
async def delete_account(
    id: int, user=Depends(user_service.validate_jwt), db: Session = Depends(get_db)
):
    return account_service.delete_account(id, db, user)
