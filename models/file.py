#!/usr/bin/env python3
"""Module for file document
"""
from mongoengine import StringField, DateTimeField, EnumField, ObjectIdField, Document, FileField
from util._enum import File_type
from datetime import datetime
from bson import ObjectId


class File(Document):
    """Define file document
    """
    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField(required=True)
    file_type = EnumField(File_type, required=True)
    file_path = FileField(required=True)
    date_modified = DateTimeField(default=datetime.now)

    meta = {
        "db_alias": "core",
        "collection": "files"
    }