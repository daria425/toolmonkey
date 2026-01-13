from tool_monkey import burst_rate_limit, with_monkey, MonkeyObserver
from agent_runtime.shared.tools import fetch_google_shop_results
if __name__ == "__main__":
    observer = MonkeyObserver()
    scenario = burst_rate_limit(on_call=3, retry_after=2.0)
    rate_limited_tool = with_monkey(
        scenario, observer)(fetch_google_shop_results)
    for i in range(1, 6):
        try:
            result = rate_limited_tool(query="laptop")
            print(f"Call {i}: ✅ Success - {result}")
        except Exception as e:
            print(f"Call {i}: ❌ RateLimitError - {e}")

    print("\n" + "=" * 50)
    print("OBSERVER METRICS:")
    print("=" * 50)
    print(observer.summary())
