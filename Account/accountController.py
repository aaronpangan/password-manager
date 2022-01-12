from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.routing import APIRouter
from typing import Optional
from uuid import uuid4
from Dto import accountDto, userDto
from sqlalchemy.orm import Session
import database
from . import accountService


router = APIRouter(prefix="/accounts", tags=["Accounts"])


get_db = database.get_db


ACCOUNTS = [
    {
        "id": "f900f41f-c32c-41e2-bc77-12610fac0236",
        "accountName": "Google",
        "password": "sadfFd45Sfd@FgjV93",
        "accountDescription": "School Email Account",
    },
    {
        "id": "f900f41f-c32c-41e2-bc77-12610fac0699",
        "accountName": "Google",
        "password": "sadfFd45Sfd@FgjV93",
        "accountDescription": "Home Email Account",
    },
    {
        "id": "f02f7ccc-f9e1-4441-8b66-c07639a8273c",
        "accountName": "Facebook",
        "password": "sadfFd45Sfd@FgjV93",
        "accountDescription": "Work Email Account",
    },
    {
        "id": "9d7c2897-b058-41ff-8f97-a824502cb8f7",
        "accountName": "Github",
        "password": "sadfFd45Sfd@FgjV93",
        "accountDescription": "Work Email Account",
    },
]


@router.get("/accounts")
async def get_accounts(searchName: Optional[str] = None, db: Session = Depends(get_db)):
    return accountService.get_accounts(searchName, db)


@router.get("/accounts/{id}")
async def get_account(id: int, db: Session = Depends(get_db)):
    account = accountService.check_account(id, db)

    return account


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def create_account(body: accountDto.CreateAccount, db: Session = Depends(get_db)):

    return accountService.create_account(body, db)


@router.put("/accounts/{id}")
async def update_account(
    id: int, body: accountDto.CreateAccount, db: Session = Depends(get_db)
):
     return accountService.update_account(id, body, db)


@router.delete("/accounts/{id}")
async def delete_account(id: int,  db: Session = Depends(get_db)):
    return accountService.delete_account(id, db)


