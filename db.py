#!/usr/bin/env python3
"""db Module
"""
from mongoengine import connect


class DB:
    """Defines connection to database
    """
    def __init__(self) -> None:
        connect(db="file_manager")    