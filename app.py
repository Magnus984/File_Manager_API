#!/usr/bin/env python3
"""FastAPI app
"""
from fastapi import FastAPI
from views.users import router as users_router
from auth import router as auth_router
from config import settings

app = FastAPI(title=settings.PROJECT_TITLE)

app.include_router(users_router)
app.include_router(auth_router)