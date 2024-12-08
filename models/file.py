#!/usr/bin/env python3
"""Module for file document
"""
from mongoengine import StringField, DateTimeField, EnumField, ObjectIdField, Document, FileField
from util._enum import Filetype
from datetime import datetime
from bson import ObjectId


class File(Document):
    """Define file document
    """
    id = ObjectIdField(primary_key=True, default=ObjectId)
    name = StringField(required=True)
    file_type = EnumField(Filetype)
    data = FileField()
    date_modified = DateTimeField(default=datetime.now)

    meta = {
        "collection": "files"
    }