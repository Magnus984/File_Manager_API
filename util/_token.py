#!/usr/bin/env python3
"""Token module
"""
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

def generate_verification_token(email: str) -> str:
    """Generates verification token
    """
    expiration = datetime.utcnow() + timedelta(minutes=10)
    payload = {
        "email": email,
        "exp": expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def confirm_verification_token(token: str) -> str:
    """Confirms verification token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")