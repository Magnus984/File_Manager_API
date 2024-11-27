#!/usr/bin/env python3
"""db Module
"""
from mongoengine import register_connection


class DB:
    """Defines connection to database
    """
    def __init__(self) -> None:
        register_connection(alias="core", name="file_manager")
