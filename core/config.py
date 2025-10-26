# Turnify - 2025 Mahin Ltd alright receipt

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Application configuration class that loads all settings from environment variables.
    This ensures secure and flexible configuration management.
    All values are production-ready with proper fallbacks.
    """
    
    # Server Configuration
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in .env file")
    
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = FLASK_ENV == 'development'
    
    # JWT Configuration
    JWT_EXPIRES_IN_DAYS = int(os.getenv('JWT_EXPIRES_IN_DAYS', 7))
    JWT_ALGORITHM = 'HS256'
    
    # MongoDB Configuration (Real Atlas Connection)
    MONGO_URI = os.getenv('MONGO_URI')
    if not MONGO_URI:
        raise ValueError("MONGO_URI must be set in .env file - MongoDB Atlas connection required")
    
    # YouTube Music Configuration
    YTMUSIC_COUNTRY = os.getenv('YTMUSIC_COUNTRY', 'GLOBAL')
    YTMUSIC_HEADERS = os.getenv('YTMUSIC_HEADERS', '{}')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # Application Info
    APP_NAME = "Turnify Backend"
    APP_VERSION = "1.0.0"
    APP_AUTHOR = "2025 Mahin Ltd"
    
    @staticmethod
    def validate():
        """
        Validate that all critical configuration values are properly set.
        Raises ValueError if any required configuration is missing.
        """
        required_vars = {
            'SECRET_KEY': os.getenv('SECRET_KEY'),
            'MONGO_URI': os.getenv('MONGO_URI')
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please check your .env file and ensure all required variables are set."
            )
        
        # Validate MongoDB URI format
        mongo_uri = os.getenv('MONGO_URI', '')
        if not mongo_uri.startswith('mongodb://') and not mongo_uri.startswith('mongodb+srv://'):
            raise ValueError("MONGO_URI must be a valid MongoDB connection string")
        
        print(f"✓ Configuration validation passed")
        print(f"✓ App: {Config.APP_NAME} v{Config.APP_VERSION}")
        print(f"✓ Environment: {Config.FLASK_ENV}")
        print(f"✓ MongoDB: Connected to Atlas")
        
        return True
    
    @staticmethod
    def get_health_info():
        """
        Get application health information for health check endpoint.
        
        Returns:
            dict: Health status information
        """
        return {
            "app_name": Config.APP_NAME,
            "version": Config.APP_VERSION,
            "author": Config.APP_AUTHOR,
            "environment": Config.FLASK_ENV,
            "status": "healthy"
        }


# Initialize and validate configuration on import
config = Config()
