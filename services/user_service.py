# Turnify - 2025 Mahin Ltd alright receipt

from bson import ObjectId
from database.mongo_client import get_collection
from database.models import UserModel, PlaylistModel, FavoriteModel


class UserService:
    """User management service"""
    
    @staticmethod
    def get_user_profile(user_id):
        """Get user profile by ID"""
        try:
            users_collection = get_collection(UserModel.COLLECTION_NAME)
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                return None, "User not found"
            
            return UserModel.sanitize_user_data(user), None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def update_user_profile(user_id, update_data):
        """Update user profile"""
        try:
            users_collection = get_collection(UserModel.COLLECTION_NAME)
            
            allowed_fields = ['display_name', 'bio', 'avatar_url']
            profile_updates = {k: v for k, v in update_data.items() if k in allowed_fields}
            
            result = users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"profile": profile_updates}}
            )
            
            if result.modified_count == 0:
                return None, "No changes made"
            
            return {"message": "Profile updated"}, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def create_playlist(user_id, name, description="", is_public=True):
        """Create a new playlist"""
        try:
            playlists_collection = get_collection(PlaylistModel.COLLECTION_NAME)
            
            playlist_doc = PlaylistModel.create_playlist_document(
                user_id, name, description, is_public
            )
            
            result = playlists_collection.insert_one(playlist_doc)
            playlist_doc['_id'] = str(result.inserted_id)
            
            return playlist_doc, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def get_user_playlists(user_id):
        """Get all playlists for a user"""
        try:
            playlists_collection = get_collection(PlaylistModel.COLLECTION_NAME)
            playlists = list(playlists_collection.find({"user_id": user_id}))
            
            for playlist in playlists:
                playlist['_id'] = str(playlist['_id'])
            
            return playlists, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def add_favorite(user_id, song_data):
        """Add song to favorites"""
        try:
            favorites_collection = get_collection(FavoriteModel.COLLECTION_NAME)
            
            favorite_doc = FavoriteModel.create_favorite_document(user_id, song_data)
            
            result = favorites_collection.insert_one(favorite_doc)
            favorite_doc['_id'] = str(result.inserted_id)
            
            return favorite_doc, None
            
        except Exception as e:
            if 'duplicate key' in str(e).lower():
                return None, "Song already in favorites"
            return None, str(e)
    
    @staticmethod
    def get_favorites(user_id):
        """Get user's favorite songs"""
        try:
            favorites_collection = get_collection(FavoriteModel.COLLECTION_NAME)
            favorites = list(favorites_collection.find({"user_id": user_id}))
            
            for fav in favorites:
                fav['_id'] = str(fav['_id'])
            
            return favorites, None
            
        except Exception as e:
            return None, str(e)
    
    @staticmethod
    def remove_favorite(user_id, song_id):
        """Remove song from favorites"""
        try:
            favorites_collection = get_collection(FavoriteModel.COLLECTION_NAME)
            
            result = favorites_collection.delete_one({
                "user_id": user_id,
                "song_id": song_id
            })
            
            if result.deleted_count == 0:
                return None, "Favorite not found"
            
            return {"message": "Removed from favorites"}, None
            
        except Exception as e:
            return None, str(e)
