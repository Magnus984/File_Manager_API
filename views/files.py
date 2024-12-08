#!/usr/bin/env python3
"""Module for file views
"""
from fastapi import APIRouter, status, HTTPException, UploadFile, File as FastAPIFile 
from pydantic import BaseModel
from models.file import File
import datetime
from util import _enum
import os
from db import DB

router = APIRouter()

conn = DB()



@router.post("/upload-file")
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
            "file_name": new_file.name,
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
##return details about files
#download files
##get files from database and store it on local system
#delete files
##delete files from database