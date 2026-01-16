import time
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Optional, Any
from tool_monkey.models import ToolCallEvent


class MonkeyObserver:
    """
    Tracks tool execution metrics during tool monkey chaos tests
    """

    def __init__(self):
        self.tool_call_events: List[ToolCallEvent] = []
        self._start_times: Dict[str, float] = {}

    def start_call(self, tool_call_id: str):
        self._start_times[tool_call_id] = time.time()

    def end_call(self, tool_name: str, tool_call_id: str, success: bool, error: Optional[Exception] = None, retry_attempt: int = 0):
        latency_ms = (
            time.time() - self._start_times.pop(tool_call_id, time.time())) * 1000
        self.tool_call_events.append(
            ToolCallEvent(
                tool_name=tool_name,
                timestamp=datetime.now(),
                success=success,
                latency_ms=latency_ms,
                error=str(error) if error else None,
                retry_attempt=retry_attempt
            )
        )

    def get_metrics(self) -> Dict[str, Any]:
        if not self.tool_call_events:
            return {}
        total = len(self.tool_call_events)
        successes = sum(1 for event in self.tool_call_events if event.success)
        failures = total - successes
        breakdown = defaultdict(
            lambda: {"call_count": 0, "failures": 0, "retries": 0})
        for event in self.tool_call_events:
            breakdown[event.tool_name]["call_count"] += 1
            if not event.success:
                breakdown[event.tool_name]["failures"] += 1
            if event.retry_attempt > 0:
                breakdown[event.tool_name]["retries"] += 1
        return {
            "total_calls": total,
            "successes": successes,
            "failures": failures,
            "success_rate": successes / total if total > 0 else 0,
            "avg_latency_ms": sum(e.latency_ms for e in self.tool_call_events) / total,
            "total_retries": sum(e.retry_attempt for e in self.tool_call_events),
            "breakdown": dict(breakdown)
        }

    def summary(self) -> str:
        """Human-readable summary."""
        metrics = self.get_metrics()
        return f"""
  Tool Monkey Execution Summary
  ==============================
  Total Calls: {metrics.get('total_calls', 0)}
  Success Rate: {metrics.get('success_rate', 0):.1%}
  Failures: {metrics.get('failures', 0)}
  Total Retries: {metrics.get('total_retries', 0)}
  Avg Latency: {metrics.get('avg_latency_ms', 0):.1f}ms
          """.strip()
