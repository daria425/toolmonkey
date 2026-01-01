from functools import wraps
from tool_monkey.models import FailureScenario
from tool_monkey.monkey import ToolMonkey


def with_monkey(failure_scenario: FailureScenario):
    monkey = ToolMonkey(failure_scenario)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            error = monkey.should_fail(func.__name__)
            if error:
                raise error
            return func(*args, **kwargs)
        return wrapper
    return decorator
