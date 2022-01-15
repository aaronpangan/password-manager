import Account.account_model as account_model
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Dto import account_dto, user_dto
import User.user_model as user_model


def get_accounts(searchName, db: Session, user: user_model.User):

    accounts = db.query(account_model.Account).filter_by(owner_Id=user.id).all()
    if searchName:
        accounts = list(
            filter(
                lambda account: searchName.lower() in account.accountName.lower(),
                accounts,
            )
        )
    return accounts


def create_account(body: account_dto.CreateAccount, db: Session, user: user_model.User):
    newAccount = account_model.Account(
        account_name=body.account_name,
        password=body.password,
        account_description=body.account_description,
        owner_Id=user.id,
    )
    db.add(newAccount)
    db.commit()
    db.refresh(newAccount)
    return newAccount


def update_account(
    id: int, body: account_dto.CreateAccount, db: Session, user: user_model.User
):
    account = check_account(id, db, user)

    account.account_name = body.account_name
    account.password = body.password
    account.account_description = body.account_description
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def delete_account(id: int, db: Session, user: user_model.User):
    check_account(id, db, user)

    account = account_model.Account
    db.query(account).filter(account.id == id, account.owner_Id == user.id).delete()

    db.commit()

    return {"msg": "Successfully Deleted"}


def check_account(id: int, db: Session, user: user_model.User):
    account = (
        db.query(account_model.Account)
        .filter(
            account_model.Account.id == id, account_model.Account.owner_Id == user.id
        )
        .first()
    )

    if account is not None:
        return account

    raise HTTPException(
        status_code=404,
        detail="Account not found",
        headers={"error": "Account ID doesn't exist"},
    )
