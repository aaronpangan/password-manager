from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from pydantic.fields import Field
from uuid import UUID, uuid4


app = FastAPI()


class Accounts(BaseModel):
    id: UUID
    accountName: str = Field(min_length=1, title="Name of the Account")
    password: str = Field(min_length=1, title="Password of the Account")
    accountDescription: Optional[str] = Field(
        "N/A", title="Description of the Account", max_length=100
    )

    class Config:
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


@app.post("/accounts")
def create_account(body: Accounts):
    body["id"] = uuid4()
    ACCOUNTS.append(body)

    return body


@app.get("/accounts")
def get_accounts(searchName: Optional[str] = None):

    if searchName:
        searchedString = []
        for account in ACCOUNTS:
            if searchName.lower() in account["accountName"].lower():
                searchedString.append(account)
        return searchedString

    return ACCOUNTS


# @app.put("/accounts/{account_id}"})
# def update_account(account_id: UUID):
