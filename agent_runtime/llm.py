from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import os
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: Dict[str, Any]


class LLMResponse(BaseModel):
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None
    raw_response: Any


class LLMProvider(ABC):
    """
    Abstract base class to use with LLM Provider SDKs
    Each concrete class must implement:
    create_completion: Make an API call with tools
    format_tool_result: Process tool result according to how tool response is returned
    """

    def __init__(self, model: str, auth: Optional[str] = None):
        self.model = model
        self.auth = auth  # api key

    @abstractmethod
    def create_completion(self, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]], **kwargs) -> LLMResponse:
        pass

    def format_tool_result(self, tool_call_id: str, result: Any) -> Dict[str, Any]:
        pass


class OpenAIProvider(LLMProvider):

    def __init__(self, model: str = "o4-mini-2025-04-16", api_key: Optional[str] = None):
        super().__init__(model, api_key)
        try:
            from openai import OpenAI

        except ImportError:
            raise ImportError("OpenAI package installation required")

        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def create_completion(self, messages, tools, **kwargs):
        """Call OpenAI Responses API with tools."""
        response = self.client.responses.create(
            model=self.model,
            input=messages,
            tools=tools,
            **kwargs  # system instructions
        )
        tool_calls = []
        content = None

        for item in response.output:
            if item.type == "function_call":
                tool_calls.append(ToolCall(
                    id=item.call_id,
                    name=item.name,
                    arguments=json.loads(item.arguments)
                ))
            elif item.type == "text":
                content = item.text

        # If no explicit text, use output_text
        if content is None and hasattr(response, 'output_text'):
            content = response.output_text

        return LLMResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
            raw_response=response
        )

    def format_tool_result(self, tool_call_id: str, result: Any) -> Dict[str, Any]:
        """Format tool result for Responses API."""
        if isinstance(result, str):
            output = result
        else:
            if hasattr(result, 'model_dump'):
                output = json.dumps(result.model_dump())
            elif hasattr(result, 'dict'):
                output = json.dumps(result.dict())
            else:
                output = json.dumps(result)

        return {
            "type": "function_call_output",
            "call_id": tool_call_id,
            "output": output
        }
