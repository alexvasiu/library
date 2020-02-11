"""
Singleton for Database connection
"""

import sqlite3

class Database: # pylint: disable=too-few-public-methods
    """
    Singleton for Database connection
    """
    __connection = None

    def __init__(self):
        if Database.__connection is not None:
            raise Exception("This is a singleton")
        Database.__connection = sqlite3.connect('db.db', check_same_thread=False)

    @staticmethod
    def connection():
        """
        Retrive the database connection
        """
        if Database.__connection is None:
            Database()
        return Database.__connection
