from tool_monkey.models import FailureScenario
from typing import Optional


class ToolMonkey:

    def __init__(self, failure_scenario: FailureScenario):
        self.failure_scenario = failure_scenario
        self.preamble = "ʕ•͡-•ʔ Tool Monkey unleashed! ʕ•͡-•ʔ"
        self.call_counts = {}

    def should_fail(self, tool_name: str) -> Optional[Exception]:
        self.call_counts[tool_name] = self.call_counts.get(tool_name, 0)+1
        for fail in self.failure_scenario.failures:
            if fail.tool_name == tool_name and fail.on_call_count == self.call_counts[tool_name]:
                return self._unleash_monkey(fail.error_type)

    def _unleash_monkey(self, error_type: str):
        if error_type == "rate_limit":
            return RuntimeError(f"{self.preamble}: Rate limit exceeded")
        elif error_type == "timeout":
            return TimeoutError(f"{self.preamble}: Request timed out")
