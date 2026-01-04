import time
from functools import wraps
from typing import Optional
from tool_monkey.models import FailureScenario
from tool_monkey.monkey import ToolMonkey
from tool_monkey.observer import MonkeyObserver


def with_monkey(failure_scenario: FailureScenario, observer: Optional[MonkeyObserver] = None):

    def decorator(func):
        tool_name = func.__name__
        monkey = ToolMonkey(failure_scenario, tool_name)

        @wraps(func)
        def wrapper(*args, **kwargs):
            tool_call_id = f"{tool_name}_{time.time()}"
            retry_attempt = kwargs.pop("_retry_attempt", 0)
            if observer:
                observer.start_call(tool_call_id)
            try:
                error = monkey.should_fail()
                if error:
                    raise error  # Just raise, let except handle logging

                result = func(*args, **kwargs)

                if observer:
                    observer.end_call(
                        tool_name, tool_call_id, success=True, retry_attempt=retry_attempt)

                return result

            except Exception as e:
                # Log ALL failures (chaos + real) here
                if observer:
                    observer.end_call(
                        tool_name, tool_call_id, success=False, error=e, retry_attempt=retry_attempt)
                raise
        return wrapper
    return decorator
