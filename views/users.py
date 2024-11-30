#!/usr/bin/env python3
"""Module of user views
"""
from fastapi import APIRouter, status, HTTPException
from models.user import User
from pydantic import BaseModel
from db import DB
from auth import _hash_password
from mongoengine import DoesNotExist
from util._mail import send_verification_email
from util._token import generate_token, confirm_token

router = APIRouter()

conn = DB()

class RegisterUser(BaseModel):
    email: str
    password: str

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
            send_verification_email(user.email, verification_url)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists but not verfied. Email verfication link sent"
                )
    except DoesNotExist:
        new_user = User(
            email=user.email,
            hashed_password=_hash_password(user.password)
        )
        new_user.save()
        token = generate_token(user.email, token_type="verification", expires_in=2)
        verification_url = f"http://127.0.0.1:8000/verify-email?token={token}"
        send_verification_email(user.email, verification_url)

        return {"email": user.email, "message": "User registered successfully. Email verification link sent"}

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
