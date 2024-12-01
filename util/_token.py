#!/usr/bin/env python3
"""Token module
"""
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

def generate_token(email: str, token_type: str, expires_in: int) -> str:
    """Generates token
    """
    expiration = datetime.utcnow() + timedelta(minutes=expires_in)
    payload = {
        "email": email,
        "type": token_type,
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def confirm_token(token: str, expected_type: str) -> str:
    """Confirms token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
        email = payload.get("email")
        token_type = payload.get("type")
        if email is None or token_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type or payload"
            )
        return email
    except jwt.ExpiredSignatureError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )
