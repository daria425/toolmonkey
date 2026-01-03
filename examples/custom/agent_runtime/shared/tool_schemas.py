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
