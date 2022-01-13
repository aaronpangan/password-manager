from typing import Optional
from pydantic.config import Extra
from pydantic.fields import Field
from pydantic import BaseModel, validator
from email_validator import validate_email, EmailNotValidError


class CreateUser(BaseModel):
    email: str = Field(min_length=8, title="Email of the User")
    password: str = Field(min_length=8, title="Password of the User")
    is_verified: Optional[bool] = Field(False)

    @validator("email")
    def verify_email(cls, value):
        validate_email(value)
        return value
