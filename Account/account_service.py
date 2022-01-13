import Account.account_model as account_model
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Dto import account_dto, user_dto


def get_accounts(searchName, db: Session):

    accounts = db.query(account_model.Account).all()

    if searchName:
        accounts = list(
            filter(
                lambda account: searchName.lower() in account.accountName.lower(),
                accounts,
            )
        )
    return accounts


def create_account(body: account_dto.CreateAccount, db: Session):
    newAccount = account_model.Account(
        account_name=body.accountName,
        password=body.password,
        account_description=body.account_description,
    )
    db.add(newAccount)
    db.commit()
    db.refresh(newAccount)
    return newAccount


def update_account(id: int, body: account_dto.CreateAccount, db: Session):
    account = check_account(id, db)

    account.account_name = body.account_name
    account.password = body.password
    account.account_description = body.account_description
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def delete_account(id: int, db: Session):
    check_account(id, db)

    db.query(account_model.Account).filter(account_model.Account.id == id).delete()

    db.commit()

    return {"msg": "Successfully Deleted"}


def check_account(id: int, db: Session):
    account = (
        db.query(account_model.Account).filter(account_model.Account.id == id).first()
    )

    if account is not None:
        return account

    raise HTTPException(
        status_code=404,
        detail="Account not found",
        headers={"error": "Account ID doesn't exist"},
    )
