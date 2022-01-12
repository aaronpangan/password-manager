from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from pydantic.config import Extra
from pydantic.fields import Field
from uuid import UUID, uuid4
import db


app = FastAPI()


class Accounts(BaseModel):
    accountName: str = Field(min_length=1, title="Name of the Account")
    password: str = Field(min_length=1, title="Password of the Account")
    accountDescription: Optional[str] = Field(
        "N/A", title="Description of the Account", max_length=100
    )

    class Config:
        extra = Extra.allow
        schema_extra = {
            "example": {
                "accountName": "Google",
                "password": "sadfFd45Sfd@FgjV93",
                "accountDescription": "School Email Account",
            }
        }


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


@app.get("/accounts")
def get_accounts(searchName: Optional[str] = None):

    if searchName:
        searchedString = []
        for account in ACCOUNTS:
            if searchName.lower() in account["accountName"].lower():
                searchedString.append(account)
        return searchedString

    return ACCOUNTS


@app.get("/accounts{id}")
def get_account(id: str):
    account = check_account(id)

    return account


@app.post("/accounts", status_code=status.HTTP_201_CREATED)
def create_account(body: Accounts):

    newAccount = {
        "id": str(uuid4()),
        "accountName": body.accountName,
        "password": body.password,
        "accountDescription": body.accountDescription,
    }

    ACCOUNTS.append(newAccount)

    return newAccount


@app.put("/accounts/{id}")
def update_account(id: str, body: Accounts):
    account = check_account(id)

    for acc in ACCOUNTS:
        if acc["id"] == account["id"]:
            acc.update(
                {
                    "accountName": body.accountName,
                    "password": body.password,
                    "accountDescription": body.accountDescription,
                }
            )
            return acc


@app.delete("/accounts/{id}")
def delete_account(id: str):
    account = check_account(id)
    if account is None:
        return {"msg": "Id not found"}

    # for index in range(len(ACCOUNTS)):
    #     if ACCOUNTS[index]["id"] == account["id"]:
    #         ACCOUNTS.pop(index)

    ACCOUNTS.remove(account)

    print(ACCOUNTS)

    return {"msg": "Successfully Deleted"}


def check_account(id: str):
    for account in ACCOUNTS:
        if id.lower() == account["id"].lower():
            return account
    raise HTTPException(
        status_code=404,
        detail="Account not found",
        headers={"error": "Account ID doesn't exist"},
    )
