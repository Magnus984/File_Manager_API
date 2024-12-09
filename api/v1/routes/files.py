#!/usr/bin/env python3
"""Module for file views
"""
from fastapi import APIRouter, status, HTTPException, UploadFile, responses, File as FastAPIFile 
from pydantic import BaseModel
from schemas.file import File
import datetime
from ..util import _enum
import os
from config.db import DB
from mongoengine import DoesNotExist
import json

router = APIRouter()

conn = DB()



@router.post("/upload")
async def upload_file(uploaded_file: UploadFile = FastAPIFile(...)):
    """Upload file of specific type and store in database
    """
    #do validation
    try:
        file_type_enum = _enum.Filetype.from_mime_type(uploaded_file.content_type)
        new_file = File(
            name=uploaded_file.filename,
            file_type=file_type_enum,
        )
        new_file.data.put(uploaded_file.file, content_type=uploaded_file.content_type)
        new_file.save()
        return {
            "message": "file created",
            "file_id": str(new_file.id),
            }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
#view files
@router.get("/view/{file_name}")
async def view_one(file_name: str):
    """View a specific file
    """
    try:
        file = File.objects(name=file_name).first()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File '{file_name}' not found"
            )
        return {
            "name": file.name,
            "file_type": file.file_type,
            "date_modified": file.date_modified
        }   
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )

#view all files
@router.get("/view")
async def view_all():
    """View all files
    """
    try:
        files = File.objects.all()
        files_list = [
            {
                "name": f.name,
                "file_type": f.file_type,
                "date_modified": f.date_modified.isoformat()
            }
            for f in files
        ]
        #return responses.JSONResponse(content={"files": files_list})
        return files_list
        #return {"files": json.dumps(files_list)}, 200
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{e}"
        )
#download files
@router.get("/download/{file_name}")
async def download_file(file_name: str):
    """Download file
    """
    try:
        file = File.objects(name=file_name).first()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File '{file_name}' not found"
            )
        return responses.StreamingResponse(
            iter([file.data.read()]),
            media_type=file.data.content_type or "application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file.name}"}
        )
    except Exception as e:
        return responses.JSONResponse(content={"error": str(e)})

#delete files
@router.get("/delete/{file_name}")
async def delete_file(file_name: str):
    """Delete flie
    """
    try:
        file = File.objects(name=file_name).first()
        if not file:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"File '{file_name}' not found"
            )
        file.data.delete()
        file.delete()
        file.save
        return {"message": "File deleted"}, 200
    except Exception as e:
        return responses.JSONResponse(content={"error": str(e)})