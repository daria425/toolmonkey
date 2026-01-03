import pytest
from tool_monkey import with_monkey, FailureScenario, ToolFailure, MonkeyObserver


def test_decorator_applies_chaos():
    """Test that decorator injects chaos on specified call."""
    scenario = FailureScenario(
        name="test",
        failures=[ToolFailure(on_call_count=1, error_type="timeout")]
    )

    @with_monkey(scenario)
    def my_func():
        return "success"

    # First call should fail
    with pytest.raises(TimeoutError):
        my_func()

    # Second call should succeed
    result = my_func()
    assert result == "success"


def test_decorator_without_observer():
    """Test that decorator works without observer."""
    scenario = FailureScenario(
        name="test",
        failures=[ToolFailure(on_call_count=2, error_type="timeout")]
    )

    @with_monkey(scenario)
    def my_func():
        return "success"

    # First call succeeds
    result = my_func()
    assert result == "success"

    # Second call fails
    with pytest.raises(TimeoutError):
        my_func()


def test_decorator_with_observer_tracks_success():
    """Test that decorator with observer tracks successful calls."""
    scenario = FailureScenario(
        name="test",
        failures=[]  # No failures
    )
    observer = MonkeyObserver()

    @with_monkey(scenario, observer=observer)
    def my_func(x):
        return x * 2

    result = my_func(5)
    assert result == 10

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["successes"] == 1
    assert metrics["failures"] == 0


def test_decorator_with_observer_tracks_chaos_failure():
    """Test that decorator with observer tracks chaos-injected failures."""
    scenario = FailureScenario(
        name="test",
        failures=[ToolFailure(on_call_count=1, error_type="timeout")]
    )
    observer = MonkeyObserver()

    @with_monkey(scenario, observer=observer)
    def my_func():
        return "success"

    # Call should fail
    with pytest.raises(TimeoutError):
        my_func()

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["successes"] == 0
    assert metrics["failures"] == 1


def test_decorator_with_observer_tracks_real_failure():
    """Test that decorator with observer tracks real function failures."""
    scenario = FailureScenario(
        name="test",
        failures=[]  # No chaos
    )
    observer = MonkeyObserver()

    @with_monkey(scenario, observer=observer)
    def my_func():
        raise ValueError("real error")

    # Function itself fails
    with pytest.raises(ValueError, match="real error"):
        my_func()

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["successes"] == 0
    assert metrics["failures"] == 1


def test_decorator_tracks_multiple_calls():
    """Test that observer tracks multiple successful and failed calls."""
    scenario = FailureScenario(
        name="test",
        failures=[ToolFailure(on_call_count=2, error_type="timeout")]
    )
    observer = MonkeyObserver()

    @with_monkey(scenario, observer=observer)
    def my_func():
        return "success"

    # Call 1: success
    my_func()

    # Call 2: chaos failure
    with pytest.raises(TimeoutError):
        my_func()

    # Call 3: success
    my_func()

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 3
    assert metrics["successes"] == 2
    assert metrics["failures"] == 1


def test_decorator_with_function_args():
    """Test that decorator works with functions that take arguments."""
    scenario = FailureScenario(name="test", failures=[])
    observer = MonkeyObserver()

    @with_monkey(scenario, observer=observer)
    def add(a, b):
        return a + b

    result = add(3, 5)
    assert result == 8

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["successes"] == 1
