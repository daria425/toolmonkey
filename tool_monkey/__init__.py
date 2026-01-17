"""Tool Monkey - Chaos testing toolkit for LLM agents.

Inspired by Netflix's Chaos Monkey, Tool Monkey helps you test agent resilience
by injecting deterministic failures at the tool boundary.
"""

from tool_monkey.models import FailureScenario, ToolFailure, ToolFailureConfigDict
from tool_monkey.monkey import ToolMonkey
from tool_monkey.decorators import with_monkey
from tool_monkey.observer import MonkeyObserver
from tool_monkey.exceptions import ToolMonkeyError, RateLimitError, AuthenticationError
from tool_monkey.config.logger import setup_default_logging, logger
from tool_monkey.scenarios.timeouts import single_timeout, retry_exhaustion, progressive_timeout, intermittent_timeout
from tool_monkey.scenarios.rate_limits import burst_rate_limit, progressive_rate_limit
from tool_monkey.scenarios.auth_failures import forbidden_access, expired_token, invalid_api_key

__version__ = "0.1.0"

__all__ = [
    "FailureScenario",
    "ToolFailure",
    "ToolMonkey",
    "MonkeyObserver",
    "ToolFailureConfigDict",
    "with_monkey",
    "ToolMonkeyError",
    "RateLimitError",
    "AuthenticationError",
    "single_timeout",
    "retry_exhaustion",
    "intermittent_timeout",
    "progressive_timeout",
    "burst_rate_limit",
    "progressive_rate_limit",
    "setup_default_logging",
    "forbidden_access",
    "invalid_api_key",
    "expired_token",
    "logger",
]
