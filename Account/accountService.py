import models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Dto import accountDto, userDto


def get_accounts(searchName, db: Session):

    accounts = db.query(models.Account).all()

    if searchName:
        accounts = list(
            filter(
                lambda account: searchName.lower() in account.accountName.lower(),
                accounts,
            )
        )
    return accounts


def create_account(body: accountDto.CreateAccount, db: Session):
    newAccount = models.Account(
        accountName=body.accountName,
        password=body.password,
        accountDescription=body.accountDescription,
    )
    db.add(newAccount)
    db.commit()
    db.refresh(newAccount)
    return newAccount


def update_account(id: int, body: accountDto.CreateAccount, db: Session):
    account = check_account(id, db)

    account.accountName=body.accountName
    account.password=body.password
    account.accountDescription=body.accountDescription
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def delete_account(id:int, db: Session):
    check_account(id, db)

    db.query(models.Account).filter(models.Account.id == id).delete()

    db.commit()

    return {'msg': 'Successfully Deleted'}


def check_account(id: int, db: Session):
    account = db.query(models.Account).filter(models.Account.id == id).first()

    if account is not None:
        return account

    raise HTTPException(
        status_code=404,
        detail="Account not found",
        headers={"error": "Account ID doesn't exist"},
    )
