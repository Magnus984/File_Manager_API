#!/usr/bin/env python3
"""Module for user views
"""
from fastapi import APIRouter, status, HTTPException, Depends, responses
from models.user import User
from pydantic import BaseModel, EmailStr
from db import DB
from auth import _hash_password
from mongoengine import DoesNotExist
from util._mail import send_verification_email
from util._token import generate_token, confirm_token
from auth import get_current_active_user
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import temp

router = APIRouter()

conn = DB()

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str


@router.get("/")
def root():
    return responses.RedirectResponse("/docs")


@router.post("/register-user", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser):
    """Registers new user
    """
    try:
        existing_user = User.objects.get(email=user.email)
        if existing_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
                )
        else:
            token = generate_token(user.email, token_type="verification", expires_in=2)
            verification_url = f"http://127.0.0.1:8000/verify-email?token={token}"
            try:
                send_verification_email(user.email, verification_url)
            except Exception:
                raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email. Please try again."
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists but not verfied. Email verfication link sent"
                )
    except DoesNotExist:
        new_user = User(
            email = user.email,
            username = user.username,
            hashed_password =_hash_password(user.password)
        )
        new_user.save()
        token = generate_token(user.email, token_type="verification", expires_in=2)
        verification_url = f"http://127.0.0.1:8000/verify-email?token={token}"
        try:
            send_verification_email(user.email, verification_url)
        except Exception:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email. Please try again."
        )

        return {
            "email": user.email,
            "username": user.username,
            "message": "User registered successfully. Email verification link sent"
            }

@router.get("/verify-email")
def verify_email(token: str):
    """Verifies email upon registration
    """
    email = confirm_token(token, expected_type="verification")
    if email:
        try:
            new_user = User.objects.get(email=email)
            new_user.is_verified = True
            new_user.save()
            return {"message": "Email verified successfully"}
        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"message": "User not found"}
                )

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    email = current_user.email
    username = current_user.username
    return {
        "username": current_user.username,
        "email": current_user.email
    }


@router.post("/reset_password")
async def reset_password(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
    """Initiates password reset by sending a verification email.
    """
    try:
        username = form_data.username
        password = form_data.password
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters"
            )
        user = User.objects.get(username=username)
        hashed_password = _hash_password(password)
        token = generate_token(user.email, token_type="verification", expires_in=10)
        temp.store_temp_data(token, hashed_password)
        verification_url = f"http://127.0.0.1:8000/change-password?token={token}"
        try:
            send_verification_email(user.email, verification_url)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send password reset email. Please try again later."
            )
        return {"message": "Password reset email sent successfully"}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )


@router.get("/change-password")
def change_password(token: str):
    """Validates the token and updates the user's password.
    """
    try:
        email = confirm_token(token, "verification")
        hashed_password = temp.retrieve_temp_data(token)
        print(f"The type of {hashed_password} is:", type(hashed_password))
        if not hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )

        user = User.objects.get(email=email)
        user.hashed_password = hashed_password.decode('utf-8')
        user.save()
        temp.delete_temp_data(token)
        return {"message": "Password updated successfully"}
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not exist"
        )