from typing import Callable, Dict, Any, Optional
from agent_runtime.llm import OpenAIProvider, LLMProvider, ToolCall
from agent_runtime.tool_registry import tool_items, ToolRegistry

from utils.logger import logger
from utils.lib import format_prompt


# llm=OpenAIProvider()
# input_list = [{"role": "user", "content": "Why am I getting 404?"}]
# response=llm.create_completion(input_list)

class AgentRuntime:
    def __init__(self, llm_provider: LLMProvider, tool_registry: ToolRegistry, tool_config: Optional[Dict[str, Any]] = None):
        self.llm = llm_provider
        self.tool_registry = tool_registry
        self.tool_config = tool_config or {}
        for t in tool_items:
            self.tool_registry.register(t)

    def _get_tool_schemas(self):
        return self.tool_registry.get_tool_schemas()

    def _execute_tool(self, tool_call: ToolCall):
        tool_item = self.tool_registry.tools[tool_call.name]
        func = tool_item.tool_implementation
        kwargs = tool_call.arguments.copy()
        if tool_call.name in self.tool_config:
            kwargs.update(self.tool_config[tool_call.name])
        return func(**kwargs)

    def run(self, user_query: str, system_instructions: str, max_steps: int = 10):
        input_list = [{"role": "user", "content": user_query}]

        for step in range(max_steps):
            # Call LLM
            response = self.llm.create_completion(
                messages=input_list,
                tools=self._get_tool_schemas(),
                instructions=system_instructions
            )
            logger.info(f"{step}: Recieved response: {response}")

            input_list += response.raw_response.output

            if not response.tool_calls:
                return response.content

            # Execute tools
            for tool_call in response.tool_calls:
                result = self._execute_tool(tool_call)
                formatted = self.llm.format_tool_result(tool_call.id, result)
                input_list.append(formatted)

        raise RuntimeError(f"Max steps ({max_steps}) reached")


if __name__ == "__main__":
    llm_provider = OpenAIProvider()
    tool_registry = ToolRegistry()
    agent_runtime = AgentRuntime(llm_provider, tool_registry, tool_config={
        "fetch_logs": {
            "log_file_path": "scenarios/logs/missing_api_key.txt"
        },
        "fetch_env": {
            "mock_env_path": "scenarios/mock_env_files/.env.api_key"
        }
    })
    user_query = "Why am I getting a 404 error?"
    result = agent_runtime.run(user_query, system_instructions=format_prompt(
        "agent_runtime/instructions/debug_agent.txt"))

    print("\n" + "="*50)
    print("FINAL RESULT:")
    print("="*50)
    print(result)
