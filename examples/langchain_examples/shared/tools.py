
from pydantic import BaseModel


class WeatherToolInput(BaseModel):
    location: str
    units: str = "celsius"


class CheckInventoryInput(BaseModel):
    product_id: str
    quantity: int


class ImageGenInput(BaseModel):
    prompt: str
    style: str


class UserPlaylistInput(BaseModel):
    user_id: str = "user123"


def base_weather_tool(location: str, units: str = "celsius"):
    """Get the current weather for a given location.
            Args:
                location (str): The location to get the weather for.
                units (str): The units to return the weather in. Either 'celsius' or 'fahrenheit'.
            Returns:
                str: The current weather in the given location.
    """
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    return result


def base_image_gen_tool(prompt: str, style: str):
    """
    Generate an image using AI (mock DALL-E, Midjourney, etc.)

    These APIs have STRICT rate limits:
    - Free tier: 5 images/minute
    - Agents asking for multiple variations would hit this fast
    Args:
        prompt (str): The text prompt describing the desired image.
        style (str): The artistic style to apply to the generated image.
    Returns:
        dict: Details of the generated image.
    """
    return {
        "image_url": f"https://fake-cdn.com/images/{hash(prompt)}.png",
        "prompt": prompt,
        "style": style,
        "generation_time": 2.3
    }


def base_search_spotify_tracks(query: str, limit: int = 5):
    """Search for tracks on Spotify.
    Args:
        query (str): The search query.
        limit (int): The number of tracks to return.
    Returns:
        dict: Search results including track details."""
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
    """Get user's Spotify playlists
    Args:
        user_id (str): The Spotify user ID.
    Returns:
        dict: User's playlists including playlist details."""
    playlists = [
        {"id": "playlist1", "name": "Workout Mix", "tracks_count": 42},
        {"id": "playlist2", "name": "Chill Vibes", "tracks_count": 28},
        {"id": "playlist3", "name": "Road Trip", "tracks_count": 65},
    ]
    return {"playlists": playlists}


def base_add_tracks_to_playlist(playlist_id: str, track_ids: list):
    """Add tracks to a Spotify playlist.
    Args:
        playlist_id (str): The ID of the playlist to add tracks to.
        track_ids (list): List of track IDs to add.
    Returns:
        dict: Confirmation of tracks added."""
    return {
        "success": True,
        "playlist_id": playlist_id,
        "tracks_added": len(track_ids)
    }


def base_get_track_recommendations(seed_track_id: str, limit: int = 10):
    """Get Spotify recommendations based on seed track
    Args:
        seed_track_id (str): The ID of the seed track.
        limit (int): The number of recommendations to return.
    Returns:
        dict: Recommended tracks based on the seed track."""
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


def base_search_products(query: str, category: str):
    """Search for products in a catalog
    Args:
        query (str): The search query.
        category (str): The product category to search in.
    Returns:
        dict: Search results including product details."""
    products = {
        "laptop": [
            {"id": "LP001", "name": "MacBook Pro",
                "price": 1999.99, "category": "electronics"},
            {"id": "LP002", "name": "Dell XPS",
             "price": 1499.99, "category": "electronics"},
        ],
        "mouse": [
            {"id": "MS001", "name": "Logitech MX",
             "price": 99.99, "category": "accessories"},
        ],
    }
    mock_db = {
        "electronics": products
    }
    # Simulate search
    items = mock_db.get(category, {})
    results = items.get(query.lower(), [])
    return {"results": results, "count": len(results)}


def base_check_inventory(product_id: str, quantity: int = 1):
    """Check product inventory
    Args:
        product_id (str): The ID of the product to check.
        quantity (int): The quantity to check for availability.
    Returns:
        dict: Inventory status including available quantity and stock status."""
    inventory = {
        "LP001": 50,
        "LP002": 30,
        "MS001": 200,
    }
    available = inventory.get(product_id, 0)
    return {
        "product_id": product_id,
        "requested": quantity,
        "available": available,
        "in_stock": available >= quantity
    }


def base_place_order(product_id: str, quantity: int, customer_email: str):
    """Place an order for a product
    Args:
        product_id (str): The ID of the product to order.
        quantity (int): The quantity to order.
        customer_email (str): The customer's email address.
    Returns:
        dict: Order confirmation details."""
    return {
        "order_id": f"ORD-{hash(product_id) % 10000}",
        "product_id": product_id,
        "quantity": quantity,
        "status": "confirmed",
        "customer_email": customer_email
    }
