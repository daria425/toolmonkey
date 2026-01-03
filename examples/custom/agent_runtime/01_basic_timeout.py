import sys
from pathlib import Path

from tool_monkey import ToolFailure, FailureScenario
# Add examples/custom to path FIRST (before other imports)
sys.path.insert(0, str(Path(__file__).parent.parent))


# Import from local example modules
from agent_runtime.shared.utils.lib import format_prompt
from agent_runtime.shared.agent_runtime import AgentRuntime
from agent_runtime.shared.tool_registry import ToolRegistry
from agent_runtime.shared.llm import OpenAIProvider


if __name__ == "__main__":
    # Get base path for examples/custom/
    base_path = Path(__file__).parent.parent
    llm_provider = OpenAIProvider()
    tool_registry = ToolRegistry()
    timeout = ToolFailure(error_type="timeout", config={
                          "timeout": {"n_seconds": 3}})
    failure_scenarios = {"fetch_logs": FailureScenario(
        name="basic_timeout",
        failures=[timeout]
    )}
    agent_runtime = AgentRuntime(llm_provider, tool_registry, tool_config={
        "fetch_logs": {
            "log_file_path": str(base_path / "scenarios/logs/missing_api_key.txt")
        },
        "fetch_env": {
            "mock_env_path": str(base_path / "scenarios/mock_env_files/.env.api_key")
        }
    }, failure_scenarios=failure_scenarios)

    user_query = "Why am I getting a 404 error?"

    try:
        result = agent_runtime.run(
            user_query,
            system_instructions=format_prompt(
                str(base_path / "agent_runtime/instructions/debug_agent.txt")),
        )

        print("\n" + "=" * 50)
        print("FINAL RESULT:")
        print("=" * 50)
        print(result)

    except Exception as e:
        print("\n" + "=" * 50)
        print("AGENT FAILED:")
        print("=" * 50)
        print(f"Error: {e}")

    finally:
        # Always print observer metrics, even if agent crashed
        print("\n" + "=" * 50)
        print("OBSERVER METRICS:")
        print("=" * 50)
        print(agent_runtime.observer.summary())
