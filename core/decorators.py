# Turnify - 2025 Mahin Ltd alright receipt

from functools import wraps
from flask import request
from core.auth import decode_jwt_token
from core.response import error_response


def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    Usage: @token_required
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return error_response("Invalid token format", status_code=401)
        
        if not token:
            return error_response("Token is missing", status_code=401)
        
        # Decode token
        payload, error = decode_jwt_token(token)
        
        if error:
            return error_response(error, status_code=401)
        
        # Add user info to request context
        request.current_user = payload
        
        return f(*args, **kwargs)
    
    return decorated
