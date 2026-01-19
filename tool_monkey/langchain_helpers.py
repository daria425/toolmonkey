from typing import Optional, Callable
from tool_monkey import FailureScenario, MonkeyObserver, with_monkey


def create_tool_with_monkey(base_tool: Callable, scenario: FailureScenario, observer: Optional[MonkeyObserver] = None, tool_name: Optional[str] = None, tool_desc: Optional[str] = None, **tool_decorator_kwargs):
    from langchain_core.tools import tool
    wrapped_tool = with_monkey(scenario, observer)(base_tool)
    tool_name = tool_name or tool_decorator_kwargs.pop(
        "name", None) or base_tool.__name__.replace("base_", "")
    if tool_desc:
        tool_decorator_kwargs["description"] = tool_desc
    elif "description" not in tool_decorator_kwargs:
        tool_decorator_kwargs["description"] = base_tool.__doc__ or f"Tool: {tool_name}"

    @tool(tool_name, **tool_decorator_kwargs)  # Unpack all kwargs
    def chaos_tool(*args, **kwargs):
        return wrapped_tool(*args, **kwargs)
    return chaos_tool


def create_agent_with_monkey(
    agent_factory: Callable,
    llm,
    base_tools: list,
    scenario: FailureScenario,
    observer: Optional[MonkeyObserver] = None,
    **agent_kwargs
):
    """
    Wrap any LangChain agent factory with chaos injection.

    Args:
        agent_factory: LangChain agent creation function (e.g., create_react_agent)
        llm: The language model to use
        base_tools: List of base tool functions to wrap with chaos
        scenario: Failure scenario to apply to all tools
        observer: Optional MonkeyObserver for tracking metrics
        **agent_kwargs: Additional kwargs passed to the agent_factory

    Returns:
        Agent with all tools wrapped in chaos injection

    Example:
        from langchain.agents import create_react_agent

        agent = create_agent_with_monkey(
            create_react_agent,
            llm,
            [base_weather_tool, base_image_gen_tool],
            burst_rate_limit(),
            observer,
            prompt=custom_prompt
        )
    """
    chaos_tools = [
        create_tool_with_monkey(tool, scenario, observer)
        for tool in base_tools
    ]
    return agent_factory(llm, chaos_tools, **agent_kwargs)
