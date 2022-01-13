import User.user_model as user_model
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Dto import account_dto, user_dto
import bcrypt


def find_user(id: int, db: Session):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()

    if user is not None:
        return user

    raise HTTPException(
        status_code=404,
        detail="User not found",
        headers={"error": "User ID doesn't exist"},
    )


def register(body: user_dto.CreateUser, db: Session):
    user = check_by_email(body.email, db)

    if user is not None:
        raise HTTPException(
            status_code=404,
            detail="Email already Exist",
            headers={"error": "Email already Exist"},
        )

    hash_password = generate_hash(body.password)

    new_user = user_model.User(email=body.email, password=hash_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return hash_password


def login(body: user_dto.CreateUser, db: Session):

    user = check_by_email(body.email, db)

    if not user or not verify_hash(body.password, user.password):
        raise HTTPException(
            status_code=404,
            detail="User not Found",
            headers={"error": "User not Found"},
        )
    return user


def check_by_email(email: str, db: Session):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()

    return user


def generate_hash(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(10))


def verify_hash(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
