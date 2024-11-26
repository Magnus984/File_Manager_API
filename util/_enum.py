#!/usr/bin/env python3
"""_enum module
"""
from enum import Enum


class File_type(Enum):
    """Defines file types
    """
    pdf = "PDF"
    png = "PNG"
    jpeg = "JPEG"
    doc = "DOC"
    docx = "DOCX" 