# Turnify - 2025 Mahin Ltd alright receipt
# Complete Music API Blueprint with public stream endpoint

from flask import Blueprint, request, Response
from core.response import success_response, error_response
from core.decorators import token_required
from services.ytmusic_service import YTMusicService
import yt_dlp
import requests

music_bp = Blueprint('music', __name__)
ytmusic_service = YTMusicService()


@music_bp.route('/search', methods=['GET'])
@token_required
def search():
    """Search for songs"""
    try:
        query = request.args.get('q')
        limit = request.args.get('limit', 20, type=int)

        if not query:
            return error_response("Query parameter 'q' is required", status_code=400)

        results, error = ytmusic_service.search_songs(query, limit)
        if error:
            return error_response(error, status_code=500)

        return success_response(f"Found {len(results)} songs", results)

    except Exception as e:
        return error_response(f"Search failed: {str(e)}", status_code=500)


@music_bp.route('/trending', methods=['GET'])
@token_required
def trending():
    """Get trending songs"""
    try:
        limit = request.args.get('limit', 20, type=int)
        results, error = ytmusic_service.get_trending(limit)

        if error:
            return error_response(error, status_code=500)

        return success_response(f"Found {len(results)} trending songs", results)

    except Exception as e:
        return error_response(f"Failed to get trending: {str(e)}", status_code=500)


# ✅ PUBLIC Stream Endpoint (No token required)
@music_bp.route('/stream/<video_id>', methods=['GET'])
def stream(video_id):
    """Public Direct Audio Stream for Flutter Player"""
    try:
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"

        # ✅ Extract best available audio stream
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            stream_url = info.get("url")

        if not stream_url:
            return error_response("No valid audio stream found", status_code=404)

        # ✅ Stream directly to Flutter Player
        def generate():
            chunk_size = 1024 * 128  # 128KB chunk
            with requests.get(stream_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        yield chunk

        return Response(
            generate(),
            mimetype="audio/mpeg",
            headers={
                "Cache-Control": "public, max-age=3600",
                "Access-Control-Allow-Origin": "*"
            },
        )

    except Exception as e:
        print(f"⚠️ Stream Error: {e}")
        return error_response(f"Failed to stream audio: {str(e)}", status_code=500)


@music_bp.route('/details/<video_id>', methods=['GET'])
@token_required
def details(video_id):
    """Get song details"""
    try:
        result, error = ytmusic_service.get_song_details(video_id)

        if error:
            return error_response(error, status_code=404)

        return success_response("Song details retrieved", result)

    except Exception as e:
        return error_response(f"Failed to get details: {str(e)}", status_code=500)
