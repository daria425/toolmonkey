from agent_runtime.shared.tool_schemas import fetch_env_tool, fetch_logs_tool
from agent_runtime.shared.tools import fetch_env, fetch_logs


class Tool:
    def __init__(self, tool_name, tool_implementation, schema_fn):
        self.tool_name = tool_name
        self.tool_implementation = tool_implementation
        self.schema_fn = schema_fn


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool: Tool):
        self.tools[tool.tool_name] = tool

    def get_tool_schemas(self):
        return [t.schema_fn() for t in self.tools.values()]


tool_items = [
    Tool(tool_name="fetch_env", tool_implementation=fetch_env,
         schema_fn=fetch_env_tool),
    Tool(tool_name="fetch_logs", tool_implementation=fetch_logs,
         schema_fn=fetch_logs_tool)
]
