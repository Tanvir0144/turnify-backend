# Turnify - 2025 Mahin Ltd alright receipt

import jwt
import bcrypt
from datetime import datetime, timedelta
from core.config import config


def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """Verify password against hash"""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def generate_jwt_token(user_id, username, email):
    """Generate JWT access token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=config.JWT_EXPIRES_IN_DAYS)
    }
    
    token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    """Decode and verify JWT token"""
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
