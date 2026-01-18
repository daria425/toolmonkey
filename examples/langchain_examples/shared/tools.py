
from pydantic import BaseModel


class WeatherToolInput(BaseModel):
    location: str
    units: str = "celsius"


def base_weather_tool(location: str, units: str = "celsius"):
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    return result


def base_image_gen_tool(prompt: str, style: str):
    """
    Generate an image using AI (mock DALL-E, Midjourney, etc.)

    These APIs have STRICT rate limits:
    - Free tier: 5 images/minute
    - Agents asking for multiple variations would hit this fast
    """
    return {
        "image_url": f"https://fake-cdn.com/images/{hash(prompt)}.png",
        "prompt": prompt,
        "style": style,
        "generation_time": 2.3
    }


def base_search_spotify_tracks(query: str, limit: int = 5):
    """Search for tracks on Spotify (mock implementation)."""
    track_templates = [
        {"id": "track1", "name": f"{query} Workout Mix",
            "artist": "DJ Fitness", "album": "Gym Anthems"},
        {"id": "track2", "name": f"Power {query}",
            "artist": "The Energy Band", "album": "Motivation"},
        {"id": "track3", "name": f"{query} Beats",
            "artist": "Beat Makers", "album": "High Energy"},
        {"id": "track4", "name": f"Intense {query}",
            "artist": "Pump Squad", "album": "Get Fit"},
        {"id": "track5", "name": f"{query} Sessions",
            "artist": "Cardio Kings", "album": "Workout Vibes"},
    ]
    selected = track_templates[:min(limit, len(track_templates))]
    return {"tracks": selected}


def base_get_user_playlists(user_id: str = "user123"):
    """Get user's Spotify playlists (requires OAuth token - mock implementation)."""
    playlists = [
        {"id": "playlist1", "name": "Workout Mix", "tracks_count": 42},
        {"id": "playlist2", "name": "Chill Vibes", "tracks_count": 28},
        {"id": "playlist3", "name": "Road Trip", "tracks_count": 65},
    ]
    return {"playlists": playlists}


def base_add_tracks_to_playlist(playlist_id: str, track_ids: list):
    """Add tracks to a Spotify playlist (requires OAuth token - mock implementation)."""
    return {
        "success": True,
        "playlist_id": playlist_id,
        "tracks_added": len(track_ids)
    }


def base_get_track_recommendations(seed_track_id: str, limit: int = 10):
    """Get Spotify recommendations based on seed track (mock implementation)."""
    rec_templates = [
        {"id": "rec1", "name": "Similar Vibe 1",
            "artist": "Recommendation Artist", "album": "Discover"},
        {"id": "rec2", "name": "Similar Vibe 2",
            "artist": "Another Artist", "album": "Weekly Mix"},
        {"id": "rec3", "name": "You Might Like This",
            "artist": "New Discovery", "album": "Fresh Finds"},
    ]
    selected = rec_templates[:min(limit, len(rec_templates))]
    return {"tracks": selected}
