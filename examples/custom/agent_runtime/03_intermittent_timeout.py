"""
  Demonstrates intermittent timeout pattern across multiple independent tool calls.
  Simulates a flaky tool that alternates between working and timing out.
"""
import sys
from pathlib import Path
from tool_monkey import MonkeyObserver, with_monkey, intermittent_timeout

sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_runtime.shared.tool_registry import ToolRegistry, tool_items

if __name__ == "__main__":
    base_path = Path(__file__).parent.parent
    tool_registry = ToolRegistry()
    observer = MonkeyObserver()
    failure_scenarios = {"fetch_logs": intermittent_timeout(num_cycles=2)}
    for t in tool_items:
        tool_registry.register(t)
    fetch_logs_func = tool_registry.get_tool_implementation("fetch_logs")
    wrapped_fetch_logs = with_monkey(
        failure_scenarios["fetch_logs"], observer)(fetch_logs_func)
    for i in range(1, 5):
        try:
            print(f"\n--- Tool Call Attempt {i} ---")
            result = wrapped_fetch_logs(reasoning="Some reasoning", confidence=0.9, log_file_path=str(
                base_path / "scenarios/logs/missing_api_key.txt"))
            print(f"Tool Call Succeeded: {result}")
        except Exception as e:
            print(f"Tool Call Failed: {e}")
    print("\n" + "=" * 50)
    print("OBSERVER METRICS:")
    print("=" * 50)
    print(observer.summary())
