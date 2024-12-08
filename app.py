#!/usr/bin/env python3
"""FastAPI app
"""
from fastapi import FastAPI
from api.v1.routes import api_router
from config.config import settings

app = FastAPI(title=settings.PROJECT_TITLE)
app.include_router(api_router, prefix="/api/v1")
