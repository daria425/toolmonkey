
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class ToolFailure(BaseModel):
    tool_name: str
    on_call_count: int
    error_type: str
    config: Optional[Dict[str, Any]] = None  # who knows u always need a config


class FailureScenario(BaseModel):
    name: str
    failures: List[ToolFailure]
