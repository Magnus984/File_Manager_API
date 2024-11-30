#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User
from util._token import generate_token, confirm_token
from fastapi import APIRouter, Depends
from mongoengine import DoesNotExist

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()


def _hash_password(password: str) -> bytes:
    """Hashes input password.
    """
    password_to_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_to_bytes, salt)
    return hashed_password



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Gets current user
    """
    email = confirm_token(token=token)
    try:
        user = User.objects.get(email=email)
        return user
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or token invalid"
        )

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = User.objects.get(form_data.username)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password_to_byte = form_data.password.encode('utf-8')
    if not bcrypt.checkpw(password_to_byte, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = generate_token(user.email, token_type="access", expires_in=30)
    return {"access_token": access_token, "token_type": "bearer"}
