"""Module with custom error responses"""


from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """Universal template for error handling"""
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """Bad request error response"""
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response
