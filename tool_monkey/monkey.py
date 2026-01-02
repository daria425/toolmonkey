import time
from tool_monkey.models import FailureScenario, TimeoutConfig, ToolFailureConfigDict
from typing import Optional


class ToolMonkey:

    def __init__(self, failure_scenario: FailureScenario):
        self.failure_scenario = failure_scenario
        self.preamble = "ʕ•͡-•ʔ Tool Monkey unleashed! ʕ•͡-•ʔ"
        self.call_counts = {}

    def should_fail(self, tool_name: str) -> Optional[Exception]:
        self.call_counts[tool_name] = self.call_counts.get(tool_name, 0) + 1
        for fail in self.failure_scenario.failures:
            if fail.tool_name == tool_name and fail.on_call_count == self.call_counts[tool_name]:
                return self._unleash_monkey(fail.error_type, fail.config)

    def _unleash_timeout(self, config: Optional[ToolFailureConfigDict] = None):
        if not config or not config.timeout:
            return TimeoutError(f"{self.preamble}: Request timed out")
        timeout_config: TimeoutConfig = config.timeout
        time.sleep(timeout_config.n_seconds)
        return TimeoutError(f"{self.preamble}: Request timed out after {timeout_config.n_seconds}")

    def _unleash_monkey(self, error_type: str, config: Optional[ToolFailureConfigDict] = None):
        if error_type == "rate_limit":
            return RuntimeError(f"{self.preamble}: Rate limit exceeded")
        elif error_type == "timeout":
            return self._unleash_timeout(config)
