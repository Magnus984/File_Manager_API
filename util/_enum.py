#!/usr/bin/env python3
"""_enum module
"""
from enum import Enum


class Filetype(Enum):
    """Defines file types
    """
    PDF = "application/pdf"
    PNG = "image/png"
    JPEG = "image/jpeg"
    DOC = "application/msword"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    @classmethod
    def from_mime_type(cls, mime_type: str):
        """Find the corresponding enum value for a MIME type."""
        for file_type in cls:
            if file_type.value == mime_type:
                print(file_type.name)
                return file_type
        raise ValueError(f"Unsupported file type: {mime_type}")