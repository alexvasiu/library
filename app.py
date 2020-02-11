"""
The main flask app
"""

import json
from flask import Flask, request
from flask_cors import CORS
from validation import validate_email_address, validate_title
from request_service import add_request, get_request, remove_request, get_all_requests

APP = Flask('library')
CORS(APP)

@APP.route('/request', methods=['POST'])
def request_add():
    """
    Implement the endpoint /request for adding a request
    """
    data = request.get_json()

    email = data.get('email')
    title = data.get('title')

    if not validate_email_address(email):
        return "Invalid email", 422

    if not validate_title(title):
        return "Invalid title", 422

    result = add_request(email, title)

    if result:
        return json.dumps(result), 201
    return "Unable to add the request", 400


@APP.route('/request/', methods=['GET'])
@APP.route('/request/<request_id>', methods=['GET'])
def request_get(request_id=None):
    """
    Implement the endpoint /request for get one request or all requests
    """
    if request_id:
        result = get_request(request_id)

        if result:
            return json.dumps(result), 200
        return f"Unable to find the request with id {request_id}", 400

    result = get_all_requests()

    if result:
        return json.dumps(result), 200
    return "Unable to fetch requests", 400


@APP.route('/request/<request_id>', methods=['DELETE'])
def request_delete(request_id):
    """
    Implement the endpoint /request for deleting a request
    """
    success = remove_request(request_id)
    if success:
        return "", 200
    return f"Unable to delete the request with id {request_id}", 400
