import time
from functools import wraps
from typing import Optional
from tool_monkey.models import FailureScenario
from tool_monkey.monkey import ToolMonkey
from tool_monkey.observer import MonkeyObserver


def with_monkey(failure_scenario: FailureScenario, observer: Optional[MonkeyObserver] = None):
    monkey = ToolMonkey(failure_scenario)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tool_call_id = f"{func.__name__}_{time.time()}"
            if observer:
                observer.start_call(tool_call_id)
            try:
                error = monkey.should_fail(func.__name__)
                if error:
                    raise error  # Just raise, let except handle logging

                result = func(*args, **kwargs)

                # if observer:
                #     observer.end_call(func.__name__, tool_call_id, success=True)

                return result

            except Exception as e:
                # Log ALL failures (chaos + real) here
                if observer:
                    observer.end_call(
                        func.__name__, tool_call_id, success=False, error=e)
                raise
        return wrapper
    return decorator
