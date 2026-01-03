import time
from typing import Optional, Dict
from tool_monkey.models import FailureScenario, TimeoutConfig, ToolFailureConfigDict, ToolFailure
from tool_monkey.config.logger import logger


class ToolMonkey:

    def __init__(self, failure_scenario: FailureScenario, tool_name: str):
        self.failure_scenario = failure_scenario
        self.preamble = "ʕ•͡-•ʔ Tool Monkey unleashed! ʕ•͡-•ʔ"
        self.tool_name = tool_name
        self.call_count = 0
        self._failure_index: Dict[int, ToolFailure] = {}
        for idx, fail in enumerate(failure_scenario.failures, start=1):
            call_num = fail.on_call_count if fail.on_call_count is not None else idx
            if call_num in self._failure_index:
                raise ValueError(f"Duplicate failure for call {call_num}")
            self._failure_index[call_num] = fail

    def should_fail(self) -> Optional[Exception]:
        self.call_count += 1
        fail = self._failure_index.get(self.call_count)
        if fail:
            return self._unleash_monkey(fail.error_type, fail.config)

    def _unleash_timeout(self, config: Optional[ToolFailureConfigDict] = None):
        if not config or not config.timeout:
            return TimeoutError(f"{self.preamble}: Request timed out")
        timeout_config: TimeoutConfig = config.timeout
        logger.info(
            "Simulating timeout for %s seconds", timeout_config.n_seconds)
        time.sleep(timeout_config.n_seconds)
        return TimeoutError(f"{self.preamble}: Request timed out after {timeout_config.n_seconds} seconds")

    def _unleash_monkey(self, error_type: str, config: Optional[ToolFailureConfigDict] = None):
        if error_type == "rate_limit":
            return RuntimeError(f"{self.preamble}: Rate limit exceeded")
        elif error_type == "timeout":
            return self._unleash_timeout(config)
