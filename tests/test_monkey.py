import pytest
from tool_monkey import ToolMonkey, FailureScenario, ToolFailure


def test_fails_on_specified_call_count():
    tool_name = "some_tool"
    tool_failure = ToolFailure(
        tool_name=tool_name, on_call_count=2, error_type="timeout"
    )
    fail_scenario = FailureScenario(
        name="test",
        failures=[tool_failure]
    )
    monkey = ToolMonkey(failure_scenario=fail_scenario)
    error = monkey.should_fail(tool_name)
    assert error is None

    error = monkey.should_fail(tool_name)
    assert error is not None
    assert isinstance(error, TimeoutError)


@pytest.mark.parametrize("error_type,expected_exception", [
    ("rate_limit", Exception),
    ("timeout", TimeoutError),
])
def test_error_type_to_exception(error_type, expected_exception):
    tool_name = "test_tool"
    tool_failure = ToolFailure(
        tool_name=tool_name, on_call_count=1, error_type=error_type
    )
    fail_scenario = FailureScenario(
        name="test",
        failures=[tool_failure]
    )
    monkey = ToolMonkey(failure_scenario=fail_scenario)

    error = monkey.should_fail(tool_name)
    assert error is not None
    assert isinstance(error, expected_exception)
