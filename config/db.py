#!/usr/bin/env python3
"""db Module
"""
from mongoengine import connect
import os

class DB:
    """Defines connection to database
    """
    def __init__(self) -> None:
        mongo_db = os.getenv("MONGO_DB", "file_manager")
        mongo_host = os.getenv("MONGO_HOST", "db") 
        mongo_port = int(os.getenv("MONGO_PORT", 27017))

        connect(
            db=mongo_db,
            host=mongo_host,
            port=mongo_port
            )    