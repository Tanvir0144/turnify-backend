# Turnify - 2025 Mahin Ltd alright receipt

import os
from flask import Flask
from flask_cors import CORS
from core.config import config
from database.models import create_indexes
from routes import register_blueprints


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config)

    # Enable CORS
    CORS(
        app,
        resources={
            r"/*": {
                "origins": config.CORS_ORIGINS.split(","),
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        }
    )

    print("\n" + "=" * 50)
    print(f"Starting {config.APP_NAME} v{config.APP_VERSION}")
    print("=" * 50)

    # Validate environment
    try:
        config.validate()
    except ValueError as e:
        print(f"✗ Configuration Error: {e}")
        raise

    # Create MongoDB indexes (safe)
    try:
        create_indexes()
    except Exception as e:
        print(f"⚠ Index creation warning: {e}")

    # Register all route blueprints
    register_blueprints(app)

    print("=" * 50)
    print(f"✓ {config.APP_NAME} is ready!")
    print(f"✓ MongoDB: {config.MONGO_URI.split('@')[-1].split('/')[0]}")
    print(f"✓ Health check: /health")
    print("=" * 50 + "\n")

    return app


# -------- Gunicorn‑visible WSGI entry point -------- #
# Gunicorn expects a variable named 'app'
app = create_app()


# -------- Local and Render runtime compatible section -------- #
if __name__ == "__main__":
    # Render provides PORT as environment variable (example: 10000)
    port = int(os.environ.get("PORT", config.PORT))  # fallback -> 5000 local
    app.run(host="0.0.0.0", port=port, debug=config.DEBUG)
