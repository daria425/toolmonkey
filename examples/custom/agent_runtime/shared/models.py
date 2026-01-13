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
    query: str
    items: List[GoogleShopItem]

# Failure scenario defs
