
from typing import Optional, Dict, Any, List, Literal
from pydantic import BaseModel
from datetime import datetime


class AuthFailureConfig(BaseModel):
    failure_type: Literal["unauthorized", "forbidden", "invalid_key"]
    status_code: int = 401
    error_message: Optional[str] = None


class TimeoutConfig(BaseModel):
    n_seconds: float


class RateLimitConfig(BaseModel):
    retry_after_seconds: float
    limit_type: Literal["per_minute", "per_hour", "burst"]
    remaining: int = 0  # 0 =exhausted


class ContentModerationConfig(BaseModel):
    # e.g., {"hate_speech": True, "violence": False}
    content_categories: Optional[Dict[str, bool]] = None
    reason: Optional[str] = None  # e.g., "Content violates policy"


class ToolFailureConfigDict(BaseModel):
    timeout: Optional[TimeoutConfig] = None
    rate_limit: Optional[RateLimitConfig] = None
    auth_failure: Optional[AuthFailureConfig] = None
    content_moderation: Optional[ContentModerationConfig] = None


class ToolFailure(BaseModel):
    # tool_name: str
    on_call_count: Optional[int] = None
    error_type: str
    # who knows u always need a config
    config: Optional[ToolFailureConfigDict] = None


class FailureScenario(BaseModel):
    name: str
    failures: List[ToolFailure]

# for observer


class ToolCallEvent(BaseModel):
    tool_name: str
    timestamp: datetime
    success: bool
    error: Optional[str] = None
    latency_ms: float
    retry_attempt: int = 0

# error type configs
