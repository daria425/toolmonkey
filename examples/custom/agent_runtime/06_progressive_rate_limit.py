import sys
from pathlib import Path
from tool_monkey import progressive_rate_limit, with_monkey, MonkeyObserver
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent_runtime.shared.llm import OpenAIProvider
from agent_runtime.shared.tool_registry import ToolRegistry, tool_items
if __name__ == "__main__":
    observer = MonkeyObserver()
    quota = 20
    scenario = progressive_rate_limit(quota=quota, retry_after=5.0)
    registry = ToolRegistry()
    llm = OpenAIProvider()
    fetch_related_queries_tool_item = next(
        t for t in tool_items if t.tool_name == "fetch_related_queries")
    registry.register(fetch_related_queries_tool_item)
    func = registry.get_tool_implementation("fetch_related_queries")
    tool_schema = next(t for t in registry.get_tool_schemas()
                       if t["name"] == "fetch_related_queries")
    rate_limited_tool = with_monkey(
        scenario, observer)(func)
    response = llm.create_completion(
        messages=[
            {"role": "user", "content": "Generate related search queries for 'laptop'."}],
        tools=[tool_schema]
    )
    print(response)
    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call.name == "fetch_related_queries":
                queries = response.tool_calls[0].arguments.get("queries", [])
                num_calls = len(queries)
                if num_calls < quota:
                    num_calls = quota + 10
                    queries.extend([""] * (num_calls - len(queries)))
                for i, q in enumerate(queries, 1):
                    try:
                        result = rate_limited_tool(query=q)
                        print(f"Call {i}: ✅ Success - {result}")
                    except Exception as e:
                        print(f"Call {i}: ❌ RateLimitError - {e}")

    print("\n" + "=" * 50)
    print("OBSERVER METRICS:")
    print("=" * 50)
    print(observer.summary())
