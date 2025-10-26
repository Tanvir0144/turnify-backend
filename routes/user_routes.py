# Turnify - 2025 Mahin Ltd alright receipt

from flask import Blueprint, request
from core.response import success_response, error_response, validation_error
from core.decorators import token_required
from services.user_service import UserService

user_bp = Blueprint('user', __name__)


@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        user_id = request.current_user.get('user_id')
        result, error = UserService.get_user_profile(user_id)
        
        if error:
            return error_response(error, status_code=404)
        
        return success_response("Profile retrieved", result)
        
    except Exception as e:
        return error_response(f"Failed to get profile: {str(e)}", status_code=500)


@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    try:
        user_id = request.current_user.get('user_id')
        data = request.get_json()
        
        if not data:
            return validation_error(["Request body is required"])
        
        result, error = UserService.update_user_profile(user_id, data)
        
        if error:
            return error_response(error, status_code=400)
        
        return success_response("Profile updated", result)
        
    except Exception as e:
        return error_response(f"Update failed: {str(e)}", status_code=500)


@user_bp.route('/playlists', methods=['GET'])
@token_required
def get_playlists():
    """Get user playlists"""
    try:
        user_id = request.current_user.get('user_id')
        result, error = UserService.get_user_playlists(user_id)
        
        if error:
            return error_response(error, status_code=500)
        
        return success_response(f"Found {len(result)} playlists", result)
        
    except Exception as e:
        return error_response(f"Failed to get playlists: {str(e)}", status_code=500)


@user_bp.route('/playlists', methods=['POST'])
@token_required
def create_playlist():
    """Create new playlist"""
    try:
        user_id = request.current_user.get('user_id')
        data = request.get_json()
        
        if not data or not data.get('name'):
            return validation_error(["Playlist name is required"])
        
        result, error = UserService.create_playlist(
            user_id,
            data.get('name'),
            data.get('description', ''),
            data.get('is_public', True)
        )
        
        if error:
            return error_response(error, status_code=400)
        
        return success_response("Playlist created", result, 201)
        
    except Exception as e:
        return error_response(f"Failed to create playlist: {str(e)}", status_code=500)


@user_bp.route('/favorites', methods=['GET'])
@token_required
def get_favorites():
    """Get user favorites"""
    try:
        user_id = request.current_user.get('user_id')
        result, error = UserService.get_favorites(user_id)
        
        if error:
            return error_response(error, status_code=500)
        
        return success_response(f"Found {len(result)} favorites", result)
        
    except Exception as e:
        return error_response(f"Failed to get favorites: {str(e)}", status_code=500)


@user_bp.route('/favorites', methods=['POST'])
@token_required
def add_favorite():
    """Add song to favorites"""
    try:
        user_id = request.current_user.get('user_id')
        data = request.get_json()
        
        if not data:
            return validation_error(["Song data is required"])
        
        result, error = UserService.add_favorite(user_id, data)
        
        if error:
            return error_response(error, status_code=400)
        
        return success_response("Added to favorites", result, 201)
        
    except Exception as e:
        return error_response(f"Failed to add favorite: {str(e)}", status_code=500)


@user_bp.route('/favorites/<song_id>', methods=['DELETE'])
@token_required
def remove_favorite(song_id):
    """Remove song from favorites"""
    try:
        user_id = request.current_user.get('user_id')
        result, error = UserService.remove_favorite(user_id, song_id)
        
        if error:
            return error_response(error, status_code=404)
        
        return success_response("Removed from favorites", result)
        
    except Exception as e:
        return error_response(f"Failed to remove favorite: {str(e)}", status_code=500)
