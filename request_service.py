"""
Request service
"""

import sqlite3
import logging
import time
from database import Database

LOGGER = logging.getLogger('library.request_service')

def add_request(email, title):
    """
    Add a request
    """
    cursor = Database.connection().cursor()
    value = None

    try:
        timestamp = str(time.time())
        cursor.execute("INSERT INTO REQUESTS(Email, Title, Timestamp) VALUES(?, ?, ?)",
                       (email, title, str(time.time())))
        value = {
            "request_id": str(cursor.lastrowid),
            "email": email,
            "title": title,
            "timestamp": timestamp
        }
    except sqlite3.Error as exception:
        LOGGER.error("Error at adding a request into the database: %s", str(exception))

    cursor.close()
    Database.connection().commit()
    return value


def get_request(request_id):
    """
    Get a request based on request_id
    """
    cursor = Database.connection().cursor()
    value = None

    try:
        cursor.execute("SELECT * FROM REQUESTS WHERE ID = ?", (request_id,))
        data = cursor.fetchone()
        if data is not None:
            value = {
                "request_id": data[0],
                "email": data[1],
                "title": data[2],
                "timestamp": data[3]
            }
    except sqlite3.Error as exception:
        LOGGER.error("Error at getting the request with id %s from the database: %s",
                     str(request_id), str(exception))

    cursor.close()
    return value


def get_all_requests():
    """
    Get all requests
    """
    cursor = Database.connection().cursor()
    values = None

    try:
        cursor.execute("SELECT * FROM REQUESTS")
        data = cursor.fetchall()
        values = []

        if data is not None:
            for row in data:
                values.append({
                    "request_id": row[0],
                    "email": row[1],
                    "title": row[2],
                    "timestamp": row[3]
                })
    except sqlite3.Error as exception:
        LOGGER.error("Error at getting all requests from the database: %s", exception)

    cursor.close()
    return values


def remove_request(request_id):
    """
    Delete a request based on request_id
    """
    cursor = Database.connection().cursor()
    done = False

    try:
        cursor.execute("DELETE FROM REQUESTS WHERE ID = ?", (request_id,))
        done = True
    except sqlite3.Error as exception:
        LOGGER.error("Error at deleting the request with id %s from the database: %s",
                     str(request_id), str(exception))

    cursor.close()
    Database.connection().commit()
    return done
