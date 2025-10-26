# Turnify - 2025 Mahin Ltd alright receipt

import re
from datetime import datetime, timedelta


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """Validate password strength (min 6 characters)"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"


def validate_username(username):
    """Validate username (3-30 characters, alphanumeric + underscore)"""
    if len(username) < 3 or len(username) > 30:
        return False, "Username must be between 3 and 30 characters"
    
    pattern = r'^[a-zA-Z0-9_]+$'
    if not re.match(pattern, username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"


def get_current_timestamp():
    """Get current UTC timestamp"""
    return datetime.utcnow()


def get_expiry_timestamp(days=7):
    """Get expiry timestamp for JWT"""
    return datetime.utcnow() + timedelta(days=days)


def sanitize_string(text, max_length=None):
    """Sanitize user input"""
    if not text:
        return ""
    
    text = text.strip()
    
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text
