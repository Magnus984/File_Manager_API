from api.v1.routes import files, users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(users.router, prefix="/user", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(files.router, prefix="/file", tags=["files"])