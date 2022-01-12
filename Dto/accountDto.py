from typing import Optional
from pydantic.config import Extra
from pydantic.fields import Field
from pydantic import BaseModel



class CreateAccount(BaseModel):
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