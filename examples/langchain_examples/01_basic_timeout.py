import sys
from pathlib import Path
from tool_monkey import MonkeyObserver, with_monkey, single_timeout
from tool_monkey.config.logger import setup_default_logging, logger
from langchain_core.tools import tool
sys.path.insert(0, str(Path(__file__).parent.parent))
from langchain_examples.shared.llm import llm
from langchain_examples.shared.tools import base_weather_tool


if __name__ == "__main__":
    # setup
    setup_default_logging(level=10)
    observer = MonkeyObserver()
    scenario = single_timeout(seconds=3.0)
    # wrap base function that will be invoked with monkey
    wrapped_base_weather_tool = with_monkey(
        scenario, observer)(base_weather_tool)

    # define a simple tool
    @tool
    def get_weather(location: str, units: str = "celcius"):
        """Get the current weather for a given location.
        Args:
            location (str): The location to get the weather for.
            units (str): The units to return the weather in. Either 'celsius' or 'fahrenheit'.
        Returns:
            str: The current weather in the given location."""
        return wrapped_base_weather_tool(location, units)

    llm_with_tool = llm.bind_tools([get_weather])
    messages = [{"role": "user", "content": "What's the weather in Boston?"}]
    logger.debug("Making LLM call with tool invocation that will timeout...")
    ai_msg = llm_with_tool.invoke(messages)
    logger.debug(f"LLM Response: {ai_msg.text}")
    messages.append(ai_msg)
    logger.debug(f"Have tool calls? {'Yes' if ai_msg.tool_calls else 'No'}")
    try:
        for tool_call in ai_msg.tool_calls:
            logger.debug(
                f"Invoking tool: {tool_call.get("name")} with args {tool_call.get('args')}")
            tool_result = get_weather.invoke(tool_call)
            logger.debug(f"Tool result: {tool_result}")
            messages.append(tool_result)
        final_response = llm_with_tool.invoke(messages)
    except Exception:
        pass
    print("\n" + "=" * 50)
    print("OBSERVER METRICS:")
    print("=" * 50)
    print(observer.summary())
