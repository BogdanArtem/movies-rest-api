"""Methods related to authentication with tokens"""


from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    """Verify user password"""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None


@basic_auth.error_handler
def basic_auth_error(status):
    """Return error message with error template"""
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    """Check if token is valid and has not expired"""
    return User.check_token(token) if token else None


@token_auth.error_handler
def token_auth_error(status):
    """Return readable error in case of authentication error"""
    return error_response(status)
