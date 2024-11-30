#!/usr/bin/env python3
"""Module for user model
"""
from mongoengine import Document, StringField, EmailField, BooleanField, ObjectIdField
from bson import ObjectId

class User(Document):
    """Defines user document
    """
    id = ObjectIdField(primary_key=True, default=ObjectId)
    username = StringField(required=True)
    email = EmailField(required=True)
    hashed_password = StringField(required=True)
    is_verified = BooleanField(default=False)
    disabled = BooleanField(default=True)

    meta = {
        "db_alias": "core",
        "collection": "users"
    }