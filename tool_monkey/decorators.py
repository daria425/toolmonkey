import time
from functools import wraps
from typing import Optional
from tool_monkey.models import FailureScenario
from tool_monkey.monkey import ToolMonkey
from tool_monkey.observer import MonkeyObserver
from tool_monkey.config.logger import logger


def with_monkey(failure_scenario: FailureScenario, observer: Optional[MonkeyObserver] = None):

    def decorator(func):
        tool_name = func.__name__
        monkey = ToolMonkey(failure_scenario, tool_name)
        call_count = {"count": 0}

        @wraps(func)
        def wrapper(*args, **kwargs):
            tool_call_id = f"{tool_name}_{time.time()}"
            # retry_attempt = kwargs.pop("_retry_attempt", 0)
            retry_attempt = call_count["count"]
            logger.debug(
                f"Tool {tool_name} called with args: {args}, kwargs: {kwargs}, attempt: {retry_attempt}")
            call_count["count"] += 1
            if observer:
                observer.start_call(tool_call_id)
            try:
                error = monkey.should_fail()
                if error:
                    raise error  # Just raise, let except handle logging

                result = func(*args, **kwargs)

                if observer:
                    logger.info(f"Ending call for {tool_name} on success")
                    observer.end_call(
                        tool_name, tool_call_id, success=True, retry_attempt=retry_attempt)
                call_count["count"] = 0

                return result

            except Exception as e:
                # Log ALL failures (chaos + real) here
                if observer:
                    logger.error("Ending call for %s after exception: %s (%s)",
                                 tool_name, e, type(e).__name__)
                    observer.end_call(
                        tool_name, tool_call_id, success=False, error=e, retry_attempt=retry_attempt)
                raise
        return wrapper
    return decorator
