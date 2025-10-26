# Turnify - 2025 Mahin Ltd alright receipt

from ytmusicapi import YTMusic
import json
import os
from core.config import config


class YTMusicService:
    """YouTube Music API service - Real production implementation (with cookies support)"""

    def __init__(self):
        try:
            # ✅ Load cookies/headers_auth.json via environment variable
            headers_path = os.getenv("YTMUSIC_HEADERS", "headers_auth.json")

            if os.path.exists(headers_path):
                self.ytmusic = YTMusic(headers_path)
                print(f"✅ YTMusic initialized with cookies file: {headers_path}")
            else:
                # Fallback - non-auth mode
                self.ytmusic = YTMusic(language='en')
                print("⚠️ headers_auth.json not found — started unauthenticated (limited mode)")

        except Exception as e:
            print(f"⚠️ YTMusic init warning: {e}")
            self.ytmusic = YTMusic(language='en')

    # 🔍 SEARCH SONGS
    def search_songs(self, query, limit=20):
        """Search for songs on YouTube Music"""
        try:
            results = self.ytmusic.search(query, filter='songs', limit=limit)

            songs = []
            for item in results:
                song = {
                    "id": item.get('videoId'),
                    "title": item.get('title', 'Unknown Title'),
                    "artist": self._get_artist_name(item),
                    "album": self._get_album_name(item),
                    "duration": item.get('duration_seconds', 0),
                    "thumbnail": self._get_thumbnail(item)
                }
                songs.append(song)

            return songs, None

        except Exception as e:
            print(f"Search error: {e}")
            return None, str(e)

    # 🔥 TRENDING
    def get_trending(self, limit=20):
        """Get trending/popular songs"""
        try:
            charts = self.ytmusic.get_charts()

            if charts and 'countries' in charts:
                trending = self._extract_trending_from_charts(charts, limit)
                if trending:
                    return trending, None

            print("⚠️ Charts unavailable — using fallback")
            return self._get_trending_fallback(limit)

        except Exception as e:
            print(f"Trending error: {e}, using fallback")
            return self._get_trending_fallback(limit)

    def _get_trending_fallback(self, limit=20):
        """Fallback method for trending"""
        try:
            trending_queries = ["top hits 2025", "viral songs", "trending music"]
            all_songs = []

            for query in trending_queries:
                results = self.ytmusic.search(query, filter='songs', limit=10)

                for item in results:
                    song = {
                        "id": item.get('videoId'),
                        "title": item.get('title', 'Unknown Title'),
                        "artist": self._get_artist_name(item),
                        "album": self._get_album_name(item),
                        "duration": item.get('duration_seconds', 0),
                        "thumbnail": self._get_thumbnail(item),
                        "views": item.get('views', 'N/A')
                    }

                    # No duplicates
                    if not any(s['id'] == song['id'] for s in all_songs):
                        all_songs.append(song)

                if len(all_songs) >= limit:
                    break

            return all_songs[:limit], None

        except Exception as e:
            print(f"Fallback trending error: {e}")
            return [], f"Unable to fetch trending songs: {str(e)}"

    def _extract_trending_from_charts(self, charts, limit):
        """Extract songs from charts"""
        try:
            trending = []
            countries = charts.get('countries', {}).get('results', [])
            for country in countries[:1]:
                for item in country.get('chart', [])[:limit]:
                    song = {
                        "id": item.get('videoId'),
                        "title": item.get('title', 'Unknown Title'),
                        "artist": self._get_artist_name(item),
                        "album": self._get_album_name(item),
                        "duration": item.get('duration_seconds', 0),
                        "thumbnail": self._get_thumbnail(item)
                    }
                    trending.append(song)
            return trending or None
        except Exception as e:
            print(f"Chart extraction error: {e}")
            return None

    # 🎧 STREAM URL
    def get_song_stream_url(self, video_id):
        """Get streaming URL for a song"""
        try:
            song_info = self.ytmusic.get_song(video_id)

            if not song_info or 'streamingData' not in song_info:
                return None, "Stream URL not available"

            formats = song_info['streamingData'].get('adaptiveFormats', [])
            audio_formats = [f for f in formats if f.get('mimeType', '').startswith('audio/')]

            if not audio_formats:
                return None, "No audio format available"

            best_audio = max(audio_formats, key=lambda x: x.get('bitrate', 0))
            return {
                "stream_url": best_audio.get('url'),
                "bitrate": best_audio.get('bitrate'),
                "mime_type": best_audio.get('mimeType'),
                "quality": best_audio.get('audioQuality', 'UNKNOWN')
            }, None

        except Exception as e:
            print(f"Stream URL error: {e}")
            return None, str(e)

    # 🧩 SONG DETAILS
    def get_song_details(self, video_id):
        """Get detailed information about a song"""
        try:
            song = self.ytmusic.get_song(video_id)
            details = song.get('videoDetails', {})

            return {
                "id": video_id,
                "title": details.get('title', 'Unknown'),
                "artist": details.get('author', 'Unknown'),
                "duration": int(details.get('lengthSeconds', 0)),
                "views": details.get('viewCount', '0'),
                "thumbnail": self._get_thumbnail_from_video_details(details),
                "description": details.get('shortDescription', '')[:200]
            }, None

        except Exception as e:
            print(f"Song details error: {e}")
            return None, str(e)

    # 🔧 Helpers
    def _get_artist_name(self, item):
        artists = item.get('artists', [])
        return artists[0].get('name', 'Unknown Artist') if artists else 'Unknown Artist'

    def _get_album_name(self, item):
        album = item.get('album')
        return album.get('name', '') if album else ''

    def _get_thumbnail(self, item):
        thumbnails = item.get('thumbnails', [])
        return thumbnails[-1].get('url', '') if thumbnails else ''

    def _get_thumbnail_from_video_details(self, video_details):
        thumbs = video_details.get('thumbnail', {}).get('thumbnails', [])
        return thumbs[-1].get('url', '') if thumbs else ''
