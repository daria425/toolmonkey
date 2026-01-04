"""Tool Monkey - Chaos testing toolkit for LLM agents.

Inspired by Netflix's Chaos Monkey, Tool Monkey helps you test agent resilience
by injecting deterministic failures at the tool boundary.
"""

from tool_monkey.models import FailureScenario, ToolFailure, ToolFailureConfigDict
from tool_monkey.monkey import ToolMonkey
from tool_monkey.decorators import with_monkey
from tool_monkey.observer import MonkeyObserver
from tool_monkey.scenarios.timeouts import late_timeout, single_timeout, retry_exhaustion, progressive_timeout

__version__ = "0.1.0"

__all__ = [
    "FailureScenario",
    "ToolFailure",
    "ToolMonkey",
    "MonkeyObserver",
    "ToolFailureConfigDict",
    "with_monkey",
    "late_timeout",
    "single_timeout",
    "retry_exhaustion",
    "progressive_timeout",
]
