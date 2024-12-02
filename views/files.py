#!/usr/bin/env python3
"""Module for file views
"""
from fastapi import APIRouter, status, HTTPException, UploadFile, File as FastAPIFile 
from pydantic import BaseModel
from models.file import File
import datetime
from util import _enum
import os

router = APIRouter()

conn = DB()

#create files
class CreateFile(BaseModel):
    name: str
    file_type: str

@router.post("/create-file")
async def create_file(file: CreateFile, uploaded_file: UploadFile = FastAPIFile(...)):
    """Creates file of specific type and store in database
    """
    #do validation
    try:
        file_type_enum = _enum.FileType.from_mime_type(uploaded_file.content_type)
        print(f"File type: {file_type_enum.name}")
        upload_path = f"/uploads/{file.name}.{file_type_enum}"
        os.makedirs("/uploads", exist_ok=True)
        #Creating and saving file on disk
        with open(upload_path, "wb") as fd:
            fd.write(await uploaded_file.read())
        #creating file object
        newfile = File(
            name = file.name,
            file_type = file_type_enum,
            file_path = upload_path,
        )
        newfile.save()
        return {
            "message": "file created",
            "file_id": str(newfile.id),
            "file_name": newfile.name,
            "file_path": newfile.file_path
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