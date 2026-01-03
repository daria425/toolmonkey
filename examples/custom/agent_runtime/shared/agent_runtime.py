
from typing import Dict, Any, Optional
from tool_monkey import FailureScenario, with_monkey, MonkeyObserver
from agent_runtime.shared.utils.logger import logger
from agent_runtime.shared.tool_registry import tool_items, ToolRegistry
from agent_runtime.shared.llm import LLMProvider, ToolCall


class AgentRuntime:
    def __init__(self, llm_provider: LLMProvider, tool_registry: ToolRegistry, tool_config: Optional[Dict[str, Any]] = None, failure_scenarios: Optional[Dict[str, FailureScenario]] = None):
        self.llm = llm_provider
        self.tool_registry = tool_registry
        self.tool_config = tool_config or {}
        self.failure_scenarios = failure_scenarios or {}
        self.observer = MonkeyObserver()
        self._tool_cache = {}

        for t in tool_items:
            self.tool_registry.register(t)

    def _get_tool_schemas(self):
        return self.tool_registry.get_tool_schemas()

    def _get_tool_function_with_wrapper(self, tool_name: str):
        if tool_name in self._tool_cache:
            return self._tool_cache[tool_name]
        tool_item = self.tool_registry.tools[tool_name]
        func = tool_item.tool_implementation
        if tool_name in self.failure_scenarios:
            scenario = self.failure_scenarios[tool_name]
            func = with_monkey(scenario, self.observer)(func)
        self._tool_cache[tool_name] = func  # store wrapped
        return func

    def _execute_tool(self, tool_call: ToolCall):
        func = self._get_tool_function_with_wrapper(tool_call.name)
        kwargs = tool_call.arguments.copy()
        if tool_call.name in self.tool_config:
            kwargs.update(self.tool_config[tool_call.name])
        return func(**kwargs)

    def run(self, user_query: str, system_instructions: str, max_steps: int = 10, handle_exceptions: bool = False):
        input_list = [{"role": "user", "content": user_query}]

        for step in range(max_steps):
            # Call LLM
            response = self.llm.create_completion(
                messages=input_list,
                tools=self._get_tool_schemas(),
                instructions=system_instructions
            )
            logger.info(
                f"{step}: Recieved response from LLM: {response.raw_response.output}")

            input_list += response.raw_response.output

            if not response.tool_calls:
                return response.content

            # Execute tools
            for tool_call in response.tool_calls:
                if handle_exceptions:
                    try:
                        tool_result = self._execute_tool(tool_call)
                        formatted = self.llm.format_tool_result(
                            tool_call.id, tool_result)
                        input_list.append(formatted)
                    except Exception as e:
                        logger.error(
                            f"Tool execution failed for {tool_call.name}: {e}")
                        error_formatted = self.llm.format_tool_result(
                            tool_call.id, f"Error: {str(e)}")
                        input_list.append(error_formatted)
                else:
                    tool_result = self._execute_tool(tool_call)
                    formatted = self.llm.format_tool_result(
                        tool_call.id, tool_result)
                    input_list.append(formatted)

        raise RuntimeError(f"Max steps ({max_steps}) reached")
