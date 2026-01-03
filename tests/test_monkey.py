import time
import pytest
from tool_monkey import ToolMonkey, FailureScenario, ToolFailure, ToolFailureConfigDict


def test_fails_on_specified_call_count():
    tool_name = "my_tool"
    tool_failure = ToolFailure(on_call_count=2, error_type="timeout"
                               )
    fail_scenario = FailureScenario(
        name="test",
        failures=[tool_failure]
    )
    monkey = ToolMonkey(failure_scenario=fail_scenario, tool_name=tool_name)
    error = monkey.should_fail()
    assert error is None

    error = monkey.should_fail()
    assert error is not None
    assert isinstance(error, TimeoutError)


@pytest.mark.parametrize("error_type,expected_exception", [
    ("rate_limit", Exception),
    ("timeout", TimeoutError),
])
def test_error_type_to_exception(error_type, expected_exception):
    tool_name = "test_tool"
    tool_failure = ToolFailure(
        on_call_count=1, error_type=error_type
    )
    fail_scenario = FailureScenario(
        name="test",
        failures=[tool_failure]
    )
    monkey = ToolMonkey(failure_scenario=fail_scenario, tool_name=tool_name)

    error = monkey.should_fail()
    assert error is not None
    assert isinstance(error, expected_exception)


def test_timeout_config():
    tool_name = "timeout_tool"
    timeout_config = ToolFailureConfigDict(
        timeout={"n_seconds": 0.1}
    )
    tool_failure = ToolFailure(on_call_count=1, error_type="timeout", config=timeout_config
                               )
    fail_scenario = FailureScenario(
        name="test",
        failures=[tool_failure]
    )
    monkey = ToolMonkey(failure_scenario=fail_scenario, tool_name=tool_name)
    start = time.time()
    error = monkey.should_fail()
    elapsed = time.time() - start
    assert error is not None
    assert elapsed >= 0.1
    assert isinstance(error, TimeoutError)
    assert "after 0.1" in str(error)
