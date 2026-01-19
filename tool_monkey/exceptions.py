"""Custom exceptions for Tool Monkey chaos scenarios."""


class ToolMonkeyError(Exception):
    """Base exception for all Tool Monkey failures."""
    pass


class RateLimitError(ToolMonkeyError):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float = 0, limit_type: str = ""):
        super().__init__(message)
        self.retry_after = retry_after
        self.limit_type = limit_type


class AuthenticationError(ToolMonkeyError):
    """Raised when authentication/authorization fails."""

    def __init__(self, message: str, failure_type: str = "unauthorized", status_code: int = 401):
        super().__init__(message)
        self.failure_type = failure_type  # "unauthorized", "forbidden", "invalid_key"
        self.status_code = status_code  # 401, 403, etc.


class ContentModerationError(ToolMonkeyError):
    """Raised when content moderation blocks the request."""

    def __init__(self, message: str, content_categories: dict = None, reason: str = ""):
        super().__init__(message)
        # e.g., {"hate_speech": True, "violence": False}
        self.content_categories = content_categories
        self.reason = reason  # e.g., "Content violates policy"
