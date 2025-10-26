# Turnify - 2025 Mahin Ltd alright receipt

from flask import Blueprint, request
from core.response import success_response, error_response, validation_error
from core.decorators import token_required
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return validation_error(["Request body is required"])
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return validation_error(["Username, email, and password are required"])
        
        result, error = AuthService.register_user(username, email, password)
        
        if error:
            return error_response(error, status_code=400)
        
        return success_response("User registered successfully", result, 201)
        
    except Exception as e:
        return error_response(f"Registration failed: {str(e)}", status_code=500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return validation_error(["Request body is required"])
        
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return validation_error(["Email and password are required"])
        
        result, error = AuthService.login_user(email, password)
        
        if error:
            return error_response(error, status_code=401)
        
        return success_response("Login successful", result)
        
    except Exception as e:
        return error_response(f"Login failed: {str(e)}", status_code=500)


@auth_bp.route('/verify', methods=['GET'])
@token_required
def verify():
    """Verify JWT token"""
    return success_response(
        "Token is valid",
        {
            "user_id": request.current_user.get('user_id'),
            "username": request.current_user.get('username'),
            "email": request.current_user.get('email')
        }
    )


@auth_bp.route('/refresh', methods=['POST'])
@token_required
def refresh():
    """Refresh JWT token"""
    from core.auth import generate_jwt_token
    
    try:
        new_token = generate_jwt_token(
            request.current_user.get('user_id'),
            request.current_user.get('username'),
            request.current_user.get('email')
        )
        
        return success_response("Token refreshed", {"token": new_token})
        
    except Exception as e:
        return error_response(f"Token refresh failed: {str(e)}", status_code=500)
