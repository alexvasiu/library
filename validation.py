"""
Validation functions
"""

import logging
import sqlite3
from email_validator import validate_email, EmailNotValidError
from database import Database

LOGGER = logging.getLogger('library.validation')

def validate_email_address(email):
    """
    Validate email
    @return True is valid, false otherwise
    """
    if email:
        try:
            validate_email(email)
            return True
        except EmailNotValidError as exception:
            LOGGER.info("email %s is not valid because", str(exception))
            return False
    return False


def validate_title(title):
    """
    Validate the title to exist
    @return True if valid, false otherwise
    """
    if title:
        cursor = Database.connection().cursor()
        result = False

        try:
            cursor.execute('SELECT * FROM TITLES WHERE Name=?', (title,))
            result = cursor.fetchone() is not None
        except sqlite3.Error as exception:
            LOGGER.error("Error at checking title into the database: %s", str(exception))

        cursor.close()
        return result
    return False
