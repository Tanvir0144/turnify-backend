# Turnify - 2025 Mahin Ltd alright receipt

from database.mongo_client import get_collection
from database.models import UserModel
from core.auth import hash_password, verify_password, generate_jwt_token
from core.utils import validate_email, validate_password, validate_username


class AuthService:
    """Authentication service - handles user registration and login"""
    
    @staticmethod
    def register_user(username, email, password):
        """Register a new user"""
        
        # Validate username
        is_valid, message = validate_username(username)
        if not is_valid:
            return None, message
        
        # Validate email
        if not validate_email(email):
            return None, "Invalid email format"
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return None, message
        
        # Check if user already exists
        users_collection = get_collection(UserModel.COLLECTION_NAME)
        
        if users_collection.find_one({"email": email.lower()}):
            return None, "Email already registered"
        
        if users_collection.find_one({"username": username}):
            return None, "Username already taken"
        
        # Hash password and create user
        hashed_password = hash_password(password)
        user_doc = UserModel.create_user_document(username, email, hashed_password)
        
        result = users_collection.insert_one(user_doc)
        user_doc['_id'] = result.inserted_id
        
        # Generate JWT token
        token = generate_jwt_token(
            str(result.inserted_id),
            username,
            email
        )
        
        return {
            "user": UserModel.sanitize_user_data(user_doc),
            "token": token
        }, None
    
    @staticmethod
    def login_user(email, password):
        """Login existing user"""
        
        users_collection = get_collection(UserModel.COLLECTION_NAME)
        user = users_collection.find_one({"email": email.lower()})
        
        if not user:
            return None, "Invalid email or password"
        
        # Verify password
        if not verify_password(password, user['password']):
            return None, "Invalid email or password"
        
        # Generate JWT token
        token = generate_jwt_token(
            str(user['_id']),
            user['username'],
            user['email']
        )
        
        return {
            "user": UserModel.sanitize_user_data(user),
            "token": token
        }, None
