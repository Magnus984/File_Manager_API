#!/usr/bin/env python3
"""Module of user views
"""
from fastapi import APIRouter, status
from models.user import User
from pydantic import BaseModel
from db import DB
from auth import _hash_password

router = APIRouter()

conn = DB()

class RegisterUser(BaseModel):
    email: str
    password: str

@router.post("/register-user")
def register_user(user: RegisterUser, status_code=status.HTTP_201_CREATED):
    new_user = User(
        email=user.email,
        hashed_password=_hash_password(user.password)
    )
    new_user.save()
    return {"email": user.email}
