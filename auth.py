#!/usr/bin/env python3
"""Authentication module.
"""
import bcrypt
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.user import User
from util._token import generate_token, confirm_token
from fastapi import APIRouter, Depends, HTTPException
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
    print("get_current_user executing")
    try:
        email = confirm_token(token=token, expected_type="access")
        try:
            user = User.objects.get(email=email)
            return user
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or token invalid"
            )
    except HTTPException as e:
        raise e

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print("get_current_active_user executing")
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        username = form_data.username
        user = User.objects.get(username=username)
    except DoesNotExist:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    password_to_byte = form_data.password.encode('utf-8')
    if not bcrypt.checkpw(password_to_byte, user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = generate_token(user.email, token_type="access", expires_in=30)
    refresh_token = generate_token(user.email, token_type="refresh", expires_in=60 * 24)
    user.disabled = False
    user.save()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
        }


@router.post("/token/refresh")
async def refresh_token(refresh_token: str):
    try:
        email = confirm_token(refresh_token, expected_type="refresh")
        new_access_token = generate_token(email, token_type="access", expires_in=30)
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired. Please log in again."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token."
        )

@router.post("/logout")
async def logout_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    """logs out current active user
    """
    current_user.disabled = True
    current_user.save()
    username = current_user.username
    return {"message": f"{current_user.username} logged out successfully"}

