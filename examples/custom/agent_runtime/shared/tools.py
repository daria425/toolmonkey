from typing import Union, Optional, List
import os
import random
from dotenv import load_dotenv
from agent_runtime.shared.models import (
    FetchedLogs, FetchedEnvVar, FetchedGoogleShopResults, GoogleShopItem,
    SpotifyTrack, SpotifySearchResults, SpotifyPlaylists, SpotifyPlaylist,
    SpotifyAddTracksResponse
)
from agent_runtime.shared.utils.logger import logger


def fetch_logs(reasoning: str, confidence: Union[int, float], num_lines: Optional[int] = None, log_file_path: Optional[str] = None):
    print(log_file_path)
    if not os.path.exists(log_file_path):
        raise RuntimeError("Log file path does not exist")
    lines = []
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()
        if num_lines:
            lines = lines[-num_lines:]
    if not lines:
        raise RuntimeError("No logs found")
    logger.info(f"Fetched {len(lines)} log lines from {log_file_path}")
    return FetchedLogs(
        reasoning=reasoning,
        confidence=confidence,
        logs=lines
    )


def fetch_env(env_var: str, reasoning: str, confidence: Union[int, float], mock_env_path: str):
    load_dotenv(dotenv_path=mock_env_path)
    fetched_env_var = os.getenv(env_var, None)
    if not fetched_env_var:
        raise RuntimeError("Environment variable not set")
    logger.info(f"Fetched environment variable {env_var}")
    return FetchedEnvVar(
        env_value=fetched_env_var,
        reasoning=reasoning,
        confidence=confidence
    )


def fetch_related_queries(query: str):
    num_items = 3
    product_templates = [
        {"name": "Wireless Bluetooth Headphones",
            "price": "$79.99", "rating": 4.5, "vendor": "TechGear"},
        {"name": "Premium Running Shoes", "price": "$129.99",
            "rating": 4.8, "vendor": "SportsPro"},
        {"name": "Stainless Steel Water Bottle",
            "price": "$24.99", "rating": 4.6, "vendor": "EcoLife"},
        {"name": "Smart Fitness Watch", "price": "$199.99",
            "rating": 4.7, "vendor": "FitTech"},
        {"name": "Portable Phone Charger", "price": "$34.99",
            "rating": 4.4, "vendor": "PowerMax"},
        {"name": "Ergonomic Laptop Stand", "price": "$49.99",
            "rating": 4.9, "vendor": "DeskPro"},
        {"name": "Noise Cancelling Earbuds", "price": "$89.99",
            "rating": 4.3, "vendor": "AudioPlus"},
        {"name": "Yoga Mat with Carry Strap", "price": "$39.99",
            "rating": 4.7, "vendor": "FitLife"},
        {"name": "LED Desk Lamp", "price": "$45.99",
            "rating": 4.5, "vendor": "BrightHome"},
        {"name": "Insulated Travel Mug", "price": "$29.99",
            "rating": 4.6, "vendor": "TravelEase"}
    ]
    selected_items = random.sample(product_templates, num_items)
    items = [GoogleShopItem(**item) for item in selected_items]

    logger.info(
        f"Fetched {len(items)}")

    return FetchedGoogleShopResults(
        items=items
    )


def search_spotify_tracks(query: str, limit: int = 5) -> SpotifySearchResults:
    """Search for tracks on Spotify (mock implementation)."""
    track_templates = [
        {"id": "track1", "name": f"{query} Workout Mix", "artist": "DJ Fitness", "album": "Gym Anthems"},
        {"id": "track2", "name": f"Power {query}", "artist": "The Energy Band", "album": "Motivation"},
        {"id": "track3", "name": f"{query} Beats", "artist": "Beat Makers", "album": "High Energy"},
        {"id": "track4", "name": f"Intense {query}", "artist": "Pump Squad", "album": "Get Fit"},
        {"id": "track5", "name": f"{query} Sessions", "artist": "Cardio Kings", "album": "Workout Vibes"},
    ]

    selected = track_templates[:min(limit, len(track_templates))]
    tracks = [SpotifyTrack(**track) for track in selected]

    logger.info(f"Found {len(tracks)} tracks matching '{query}'")

    return SpotifySearchResults(tracks=tracks)


def get_user_playlists(user_id: str = "user123") -> SpotifyPlaylists:
    """Get user's Spotify playlists (requires OAuth token - mock implementation)."""
    playlists = [
        SpotifyPlaylist(id="playlist1", name="Workout Mix", tracks_count=42),
        SpotifyPlaylist(id="playlist2", name="Chill Vibes", tracks_count=28),
        SpotifyPlaylist(id="playlist3", name="Road Trip", tracks_count=65),
    ]

    logger.info(f"Fetched {len(playlists)} playlists for user {user_id}")

    return SpotifyPlaylists(playlists=playlists)


def add_tracks_to_playlist(playlist_id: str, track_ids: List[str]) -> SpotifyAddTracksResponse:
    """Add tracks to a Spotify playlist (requires OAuth token - mock implementation)."""
    logger.info(f"Added {len(track_ids)} tracks to playlist {playlist_id}")

    return SpotifyAddTracksResponse(
        success=True,
        playlist_id=playlist_id,
        tracks_added=len(track_ids)
    )


def get_track_recommendations(seed_track_id: str, limit: int = 10) -> SpotifySearchResults:
    """Get Spotify recommendations based on seed track (mock implementation)."""
    rec_templates = [
        {"id": "rec1", "name": "Similar Vibe 1", "artist": "Recommendation Artist", "album": "Discover"},
        {"id": "rec2", "name": "Similar Vibe 2", "artist": "Another Artist", "album": "Weekly Mix"},
        {"id": "rec3", "name": "You Might Like This", "artist": "New Discovery", "album": "Fresh Finds"},
    ]

    selected = rec_templates[:min(limit, len(rec_templates))]
    tracks = [SpotifyTrack(**track) for track in selected]

    logger.info(f"Generated {len(tracks)} recommendations based on track {seed_track_id}")

    return SpotifySearchResults(tracks=tracks)
