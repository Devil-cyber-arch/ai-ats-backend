from fastapi import APIRouter

from app.database import SessionLocal
from app.models.user_model import User

from app.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()

@router.post("/register")
def register(user_data: dict):

    db = SessionLocal()

    hashed_password = hash_password(
        user_data["password"]
    )

    new_user = User(
        username=user_data["username"],
        email=user_data["email"],
        password=hashed_password,
        role=user_data["role"]
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    db.close()

    return {
        "message": "User registered successfully"
    }
@router.post("/login")
def login(user_data: dict):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == user_data["email"]
    ).first()

    if not user:

        db.close()

        return {
            "error": "Invalid email"
        }

    valid_password = verify_password(
        user_data["password"],
        user.password
    )

    if not valid_password:

        db.close()

        return {
            "error": "Invalid password"
        }

    access_token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    db.close()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }