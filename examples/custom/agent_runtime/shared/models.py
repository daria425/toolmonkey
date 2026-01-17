from typing import List, Union
from pydantic import BaseModel

# Tool responses


class FetchedLogs(BaseModel):
    reasoning: str
    confidence: Union[int, float]
    logs: List[str]


class FetchedEnvVar(BaseModel):
    env_value: str
    reasoning: str
    confidence: Union[int, float]


class GoogleShopItem(BaseModel):
    name: str
    price: str
    rating: float
    vendor: str


class FetchedGoogleShopResults(BaseModel):
    items: List[GoogleShopItem]


class SpotifyTrack(BaseModel):
    id: str
    name: str
    artist: str
    album: str = "Unknown Album"


class SpotifyPlaylist(BaseModel):
    id: str
    name: str
    tracks_count: int


class SpotifySearchResults(BaseModel):
    tracks: List[SpotifyTrack]


class SpotifyPlaylists(BaseModel):
    playlists: List[SpotifyPlaylist]


class SpotifyAddTracksResponse(BaseModel):
    success: bool
    playlist_id: str
    tracks_added: int


# Failure scenario defs
