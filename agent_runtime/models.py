from typing import List, Union
from pydantic import BaseModel


class FetchedLogs(BaseModel):
    reasoning: str
    confidence: Union[int, float]
    logs: List[str]


class FetchedEnvVar(BaseModel):
    env_value: str
    reasoning: str
    confidence: Union[int, float]
