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
