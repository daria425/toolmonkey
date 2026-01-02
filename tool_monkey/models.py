
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime


class TimeoutConfig(BaseModel):
    n_seconds: float


class ToolFailureConfigDict(BaseModel):
    timeout: Optional[TimeoutConfig] = None


class ToolFailure(BaseModel):
    tool_name: str
    on_call_count: int
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
