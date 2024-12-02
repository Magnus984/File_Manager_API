#!/usr/bin/env python3
"""_enum module
"""
from enum import Enum


class File_type(Enum):
    """Defines file types
    """
    pdf = "application/pdf"
    png = "image/png"
    jpeg = "image/jpeg"
    doc = "application/msword"
    docx = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    @classmethod
    def from_mime_type(cls, mime_type: str):
        """Find the corresponding enum value for a MIME type."""
        for file_type in cls:
            if file_type.value == mime_type:
                return file_type
        raise ValueError(f"Unsupported file type: {mime_type}")