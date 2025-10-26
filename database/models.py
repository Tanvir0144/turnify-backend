# Turnify - 2025 Mahin Ltd alright receipt

from datetime import datetime
from bson import ObjectId


class UserModel:
    """User data model"""
    
    COLLECTION_NAME = "users"
    
    @staticmethod
    def create_user_document(username, email, hashed_password):
        return {
            "username": username,
            "email": email.lower(),
            "password": hashed_password,
            "profile": {
                "display_name": username,
                "bio": "",
                "avatar_url": ""
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }
    
    @staticmethod
    def sanitize_user_data(user_doc):
        if not user_doc:
            return None
        
        user_doc['_id'] = str(user_doc['_id'])
        user_doc.pop('password', None)
        
        if 'created_at' in user_doc:
            user_doc['created_at'] = user_doc['created_at'].isoformat()
        if 'updated_at' in user_doc:
            user_doc['updated_at'] = user_doc['updated_at'].isoformat()
        
        return user_doc


class PlaylistModel:
    """Playlist data model"""
    
    COLLECTION_NAME = "playlists"
    
    @staticmethod
    def create_playlist_document(user_id, name, description="", is_public=True):
        return {
            "user_id": user_id,
            "name": name,
            "description": description,
            "is_public": is_public,
            "songs": [],
            "thumbnail": "",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }


class FavoriteModel:
    """Favorite songs model"""
    
    COLLECTION_NAME = "favorites"
    
    @staticmethod
    def create_favorite_document(user_id, song_data):
        return {
            "user_id": user_id,
            "song_id": song_data.get("id"),
            "title": song_data.get("title"),
            "artist": song_data.get("artist", "Unknown"),
            "duration": song_data.get("duration", 0),
            "thumbnail": song_data.get("thumbnail", ""),
            "added_at": datetime.utcnow()
        }


class HistoryModel:
    """Listening history model"""
    
    COLLECTION_NAME = "history"
    
    @staticmethod
    def create_history_document(user_id, song_data):
        return {
            "user_id": user_id,
            "song_id": song_data.get("id"),
            "title": song_data.get("title"),
            "artist": song_data.get("artist", "Unknown"),
            "played_at": datetime.utcnow()
        }


def create_indexes():
    """Create database indexes"""
    from database.mongo_client import get_collection
    
    try:
        users = get_collection(UserModel.COLLECTION_NAME)
        users.create_index("email", unique=True)
        users.create_index("username", unique=True)
        
        playlists = get_collection(PlaylistModel.COLLECTION_NAME)
        playlists.create_index("user_id")
        
        favorites = get_collection(FavoriteModel.COLLECTION_NAME)
        favorites.create_index([("user_id", 1), ("song_id", 1)], unique=True)
        
        history = get_collection(HistoryModel.COLLECTION_NAME)
        history.create_index([("user_id", 1), ("played_at", -1)])
        
        print("✓ Database indexes created")
        
    except Exception as e:
        print(f"⚠ Index creation warning: {e}")
