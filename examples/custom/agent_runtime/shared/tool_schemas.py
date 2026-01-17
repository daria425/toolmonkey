def fetch_logs_tool():
    tool = {
        "type": "function",
        "name": "fetch_logs",
        "description": "Fetches recent application logs to help diagnose issues. Call this when you need to inspect log entries to answer the user's query.",
        "parameters": {
            "type": "object",
            "properties": {
                "reasoning": {
                    "type": "string",
                    "description": "Explain why you believe logs should be checked to answer the user's query"
                },
                "confidence": {
                    "type": "number",
                    "description": "Your confidence level (0-1) that checking logs will help answer the query"
                }
            },
            "required": ["reasoning", "confidence"],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool


def fetch_env_tool():
    tool = {
        "type": "function",
        "name": "fetch_env",
        "description": "Fetches the value of a specified environment variable. Use this when you need to retrieve configuration or system information from environment variables.",
        "parameters": {
            "type": "object",
            "properties": {
                "env_var": {
                    "type": "string",
                    "description": "The name of the environment variable to fetch (e.g., 'LOG_PATH', 'API_KEY', 'DATABASE_URL')"
                },
                "reasoning": {
                    "type": "string",
                    "description": "Explain why you need to fetch this environment variable"
                },
                "confidence": {
                    "type": "number",
                    "description": "Your confidence level (0-1) that fetching this environment variable will help answer the query"
                }
            },
            "required": ["env_var", "reasoning", "confidence"
                         ],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool


def fetch_related_queries_tool():
    """Returns a list of related search queries to help users conduct deeper research."""
    tool = {
        "type": "function",
        "name": "fetch_related_queries",
        "description": (
            "Generates a list of related search queries based on a user's original search. "
            "Use this to help users explore a topic more deeply by suggesting similar or "
            "complementary search terms."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "original_query": {
                    "type": "string",
                    "description": (
                        "The user's original search query to generate related queries for "
                        "(e.g., 'machine learning', 'climate change', 'python async')"
                    )
                },
                "queries": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "A list of related search queries"
                }
            },
            "required": ["original_query", "queries"],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool


def search_spotify_tracks_tool():
    """Search for tracks on Spotify."""
    tool = {
        "type": "function",
        "name": "search_spotify_tracks",
        "description": "Search for songs, artists, or albums on Spotify. Use this when the user wants to find specific music.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query (e.g., 'workout music', 'Taylor Swift', 'chill vibes')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tracks to return (default: 5)"
                }
            },
            "required": ["query"],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool


def get_user_playlists_tool():
    """Get user's Spotify playlists (requires OAuth)."""
    tool = {
        "type": "function",
        "name": "get_user_playlists",
        "description": "Get the user's existing Spotify playlists. Requires OAuth authentication. Use this to see what playlists the user has.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The Spotify user ID (default: 'user123')"
                }
            },
            "required": [],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool


def add_tracks_to_playlist_tool():
    """Add tracks to a Spotify playlist (requires OAuth)."""
    tool = {
        "type": "function",
        "name": "add_tracks_to_playlist",
        "description": "Add tracks to a specific Spotify playlist. Requires OAuth authentication. Use this after finding tracks to add them to a playlist.",
        "parameters": {
            "type": "object",
            "properties": {
                "playlist_id": {
                    "type": "string",
                    "description": "The ID of the playlist to add tracks to"
                },
                "track_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of track IDs to add to the playlist"
                }
            },
            "required": ["playlist_id", "track_ids"],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool


def get_track_recommendations_tool():
    """Get Spotify recommendations based on a seed track."""
    tool = {
        "type": "function",
        "name": "get_track_recommendations",
        "description": "Get personalized song recommendations based on a seed track. Use this to discover new music similar to a specific song.",
        "parameters": {
            "type": "object",
            "properties": {
                "seed_track_id": {
                    "type": "string",
                    "description": "The ID of the seed track to base recommendations on"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of recommendations to return (default: 10)"
                }
            },
            "required": ["seed_track_id"],
            "additionalProperties": False
        },
        "strict": True
    }
    return tool
