import pytest
import time
from tool_monkey import MonkeyObserver


def test_observer_tracks_successful_call():
    """Test that observer correctly tracks a successful tool call."""
    observer = MonkeyObserver()

    observer.start_call("call_1")
    time.sleep(0.01)  # Simulate some work
    observer.end_call("my_tool", "call_1", success=True)

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["successes"] == 1
    assert metrics["failures"] == 0
    assert metrics["success_rate"] == 1.0
    assert metrics["avg_latency_ms"] > 0


def test_observer_tracks_failed_call():
    """Test that observer correctly tracks a failed tool call."""
    observer = MonkeyObserver()

    observer.start_call("call_1")
    observer.end_call("my_tool", "call_1", success=False, error=TimeoutError("timeout"))

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 1
    assert metrics["successes"] == 0
    assert metrics["failures"] == 1
    assert metrics["success_rate"] == 0.0


def test_observer_tracks_multiple_calls():
    """Test that observer tracks multiple tool calls correctly."""
    observer = MonkeyObserver()

    # 2 successes
    observer.start_call("call_1")
    observer.end_call("tool_a", "call_1", success=True)

    observer.start_call("call_2")
    observer.end_call("tool_b", "call_2", success=True)

    # 1 failure
    observer.start_call("call_3")
    observer.end_call("tool_a", "call_3", success=False, error=RuntimeError("error"))

    metrics = observer.get_metrics()
    assert metrics["total_calls"] == 3
    assert metrics["successes"] == 2
    assert metrics["failures"] == 1
    assert metrics["success_rate"] == pytest.approx(2/3, rel=0.01)


def test_observer_breakdown_by_tool():
    """Test that observer correctly breaks down metrics by tool."""
    observer = MonkeyObserver()

    # tool_a: 2 calls, 1 failure
    observer.start_call("call_1")
    observer.end_call("tool_a", "call_1", success=True)

    observer.start_call("call_2")
    observer.end_call("tool_a", "call_2", success=False, error=RuntimeError("error"))

    # tool_b: 1 call, 0 failures
    observer.start_call("call_3")
    observer.end_call("tool_b", "call_3", success=True)

    metrics = observer.get_metrics()
    breakdown = metrics["breakdown"]

    assert breakdown["tool_a"]["call_count"] == 2
    assert breakdown["tool_a"]["failures"] == 1

    assert breakdown["tool_b"]["call_count"] == 1
    assert breakdown["tool_b"]["failures"] == 0


def test_observer_tracks_retries():
    """Test that observer tracks retry attempts."""
    observer = MonkeyObserver()

    # First attempt fails
    observer.start_call("call_1")
    observer.end_call("my_tool", "call_1", success=False, error=TimeoutError("timeout"), retry_attempt=0)

    # Retry succeeds
    observer.start_call("call_2")
    observer.end_call("my_tool", "call_2", success=True, retry_attempt=1)

    metrics = observer.get_metrics()
    assert metrics["total_retries"] == 1


def test_observer_empty_metrics():
    """Test that observer returns empty dict when no calls tracked."""
    observer = MonkeyObserver()

    metrics = observer.get_metrics()
    assert metrics == {}


def test_observer_summary_format():
    """Test that summary returns a formatted string."""
    observer = MonkeyObserver()

    observer.start_call("call_1")
    observer.end_call("my_tool", "call_1", success=True)

    summary = observer.summary()
    assert "Total Calls: 1" in summary
    assert "Success Rate:" in summary
    assert "Failures: 0" in summary
