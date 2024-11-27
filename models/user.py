#!/usr/bin/env python3
"""Module for user model
"""
from mongoengine import Document, StringField, EmailField, ObjectIdField
from bson import ObjectId

class User(Document):
    """Defines user document
    """
    id = ObjectIdField(primary_key=True, default=ObjectId)
    email = EmailField(required=True)
    hashed_password = StringField(required=True)
    session_id = StringField(null=True)

    meta = {
        "db_alias": "core",
        "collection": "users"
    }