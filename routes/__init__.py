# Turnify - 2025 Mahin Ltd alright receipt

from flask import Blueprint
from core.config import config
from core.response import success_response
from database.mongo_client import mongo_db

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return success_response(
        message="Welcome to Turnify Backend API",
        data={
            "app_name": config.APP_NAME,
            "version": config.APP_VERSION,
            "author": config.APP_AUTHOR,
            "status": "running",
            "endpoints": {
                "health": "/health",
                "auth": "/auth/*",
                "music": "/music/*",
                "user": "/user/*"
            }
        }
    )


@main_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        db = mongo_db.get_db()
        db.command('ping')
        
        health_data = config.get_health_info()
        health_data['database'] = {
            "status": "connected",
            "name": db.name
        }
        
        return success_response("Server is healthy", health_data)
        
    except Exception as e:
        return success_response(
            "Server running but database issue",
            {**config.get_health_info(), "database": {"status": "error", "error": str(e)}},
            503
        )


def register_blueprints(app):
    """Register all blueprints"""
    from routes.auth_routes import auth_bp
    from routes.music_routes import music_bp
    from routes.user_routes import user_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(music_bp, url_prefix='/music')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    print("✓ All blueprints registered")


__all__ = ['register_blueprints', 'main_bp']
