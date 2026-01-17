from agent_runtime.shared.tool_schemas import (
    fetch_env_tool, fetch_logs_tool, fetch_related_queries_tool,
    search_spotify_tracks_tool, get_user_playlists_tool,
    add_tracks_to_playlist_tool, get_track_recommendations_tool
)
from agent_runtime.shared.tools import (
    fetch_env, fetch_logs, fetch_related_queries,
    search_spotify_tracks, get_user_playlists,
    add_tracks_to_playlist, get_track_recommendations
)


class Tool:
    def __init__(self, tool_name, tool_implementation, schema_fn):
        self.tool_name = tool_name
        self.tool_implementation = tool_implementation
        self.schema_fn = schema_fn


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool):
        self.tools[tool.tool_name] = tool

    def get_tool_schemas(self):
        return [t.schema_fn() for t in self.tools.values()]

    def get_tool_implementation(self, tool_name: str):
        return self.tools[tool_name].tool_implementation


tool_items = [
    Tool(tool_name="fetch_env", tool_implementation=fetch_env,
         schema_fn=fetch_env_tool),
    Tool(tool_name="fetch_logs", tool_implementation=fetch_logs,
         schema_fn=fetch_logs_tool),
    Tool(tool_name="fetch_related_queries",
         tool_implementation=fetch_related_queries, schema_fn=fetch_related_queries_tool),
    Tool(tool_name="search_spotify_tracks",
         tool_implementation=search_spotify_tracks, schema_fn=search_spotify_tracks_tool),
    Tool(tool_name="get_user_playlists",
         tool_implementation=get_user_playlists, schema_fn=get_user_playlists_tool),
    Tool(tool_name="add_tracks_to_playlist",
         tool_implementation=add_tracks_to_playlist, schema_fn=add_tracks_to_playlist_tool),
    Tool(tool_name="get_track_recommendations",
         tool_implementation=get_track_recommendations, schema_fn=get_track_recommendations_tool),
]
