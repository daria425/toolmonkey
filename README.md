# Tool Monkey

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

Chaos testing toolkit for LLM agents. Inject deterministic failures into tool calls to test error handling, retry logic, and agent resilience.

## Installation

```bash
pip install tool-monkey  # Coming soon
```

For now (install from source):
```bash
git clone https://github.com/daria425/tool-monkey
cd tool-monkey
pip install -e .
```

## What It Does

Tool Monkey wraps your tool functions and injects failures at deterministic points (e.g., "fail on 3rd call", "timeout after 2 seconds"). Use it to test how your LLM agents handle:

- Timeouts
- Rate limits
- Authentication failures
- Content moderation errors

All failures are **deterministic** - same scenario produces same failures every time.

---

## Three Ways to Use It

### 1. Manual Decorator (`with_monkey`)

**Use when:** You need full control, or want to add retry logic with libraries like `tenacity`.

```python
from tool_monkey import with_monkey, single_timeout, MonkeyObserver
from langchain_core.tools import tool
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

# Setup
observer = MonkeyObserver()
scenario = single_timeout(seconds=3.0)

# Your base function
def base_weather_tool(location: str, units: str = "celsius"):
    return f"Weather in {location}: 72°{units[0].upper()}"

# Layer 1: Wrap with chaos
wrapped_tool = with_monkey(scenario, observer)(base_weather_tool)

# Layer 2: Add retry logic
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.2, max=2.0)
)
def weather_with_retry(location: str, units: str = "celsius"):
    return wrapped_tool(location, units)

# Layer 3: Create LangChain tool
@tool
def get_weather(location: str, units: str = "celsius"):
    """Get current weather for a location."""
    return weather_with_retry(location, units)

# Use it
llm_with_tools = llm.bind_tools([get_weather])
# First call times out, retry succeeds
```

**Key:** Retry wrapper must go **between** chaos wrapper and `@tool` decorator to catch failures.

---

### 2. Tool Helper (`create_tool_with_monkey`)

**Use when:** You just want a chaos-wrapped LangChain tool without retry logic.

```python
from tool_monkey import create_tool_with_monkey, burst_rate_limit, MonkeyObserver
from pydantic import BaseModel

# Define Pydantic schema (REQUIRED for LangChain tools)
class WeatherInput(BaseModel):
    location: str
    units: str = "celsius"

# Setup
observer = MonkeyObserver()
scenario = burst_rate_limit(on_call=3, retry_after=5.0)

# Your base function
def base_weather_tool(location: str, units: str = "celsius"):
    return f"Weather in {location}: 72°{units[0].upper()}"

# Create chaos-wrapped tool in one line
get_weather = create_tool_with_monkey(
    base_weather_tool,
    scenario,
    observer,
    args_schema=WeatherInput  # Required!
)

# Use it
llm_with_tools = llm.bind_tools([get_weather])
# Fails on 3rd call with RateLimitError
```

**Important:** `args_schema` must be provided - it's passed to LangChain's `@tool` decorator internally.

---

### 3. Agent Helper (`create_agent_with_monkey`)

**Use when:** You want to wrap **all tools** in an agent with the same chaos scenario.

```python
from tool_monkey import create_agent_with_monkey, expired_token, MonkeyObserver
from langchain.agents import create_react_agent

# Setup
observer = MonkeyObserver()
scenario = expired_token(on_call=5)

# Your base tools
def base_search(query: str):
    return f"Results for {query}"

def base_weather(location: str):
    return f"Weather in {location}"

# Create agent with chaos on all tools
agent = create_agent_with_monkey(
    create_react_agent,  # Any LangChain agent factory
    llm,
    [base_search, base_weather],  # All tools get wrapped
    scenario,
    observer,
    prompt=custom_prompt  # Any agent kwargs
)

# Token expires on 5th tool call (any tool)
```

---

## Available Scenarios

### Timeouts
```python
from tool_monkey import (
    single_timeout,         # Timeout once on Nth call
    retry_exhaustion,       # Timeout N times in a row
    intermittent_timeout,   # Timeout every Nth call
    progressive_timeout,    # Timeouts get longer each time
)

scenario = single_timeout(seconds=3.0, on_call=1)
scenario = retry_exhaustion(num_failures=3, seconds=2.0)
```

### Rate Limits
```python
from tool_monkey import (
    burst_rate_limit,       # Hit limit after N calls
    progressive_rate_limit, # Quota decreases over time
)

scenario = burst_rate_limit(on_call=3, retry_after=5.0)
```

### Authentication
```python
from tool_monkey import (
    expired_token,      # Token expires on Nth call
    forbidden_access,   # 403 Forbidden
    invalid_api_key,    # Invalid API key
)

scenario = expired_token(on_call=5)
```

### Content Moderation
```python
from tool_monkey import content_policy_violation

scenario = content_policy_violation(reason="nsfw_content")
```

---

## Observability

Track metrics with `MonkeyObserver`:

```python
from tool_monkey import MonkeyObserver

observer = MonkeyObserver()

# ... run your agent ...

# Print summary
print(observer.summary())
```

**Output:**
```
Tool Monkey Execution Summary
==============================
Total Calls: 5
Success Rate: 60.0%
Failures: 2
Total Retries: 2
Avg Latency: 1523.4ms
```

---

## Custom Scenarios

Build your own:

```python
from tool_monkey import FailureScenario, ToolFailure

scenario = FailureScenario(
    name="custom_chaos",
    failures=[
        ToolFailure(
            error_type="timeout",
            on_call_count=1,
            config={"timeout": {"n_seconds": 5.0}}
        ),
        ToolFailure(
            error_type="rate_limit",
            on_call_count=3,
            config={"rate_limit": {"retry_after": 10.0}}
        ),
    ]
)
```

---

## Examples

See `examples/langchain_examples/` for full notebooks:

- `01_single_timeout.ipynb` - Basic timeout, retry patterns
- `02_retry_exhaustion.ipynb` - Tenacity retry exhaustion
- `03_rate_limits.ipynb` - Image generation with rate limits
- `04_auth_failures.ipynb` - OAuth token expiration
- `05_content_moderation.ipynb` - Content policy violations (image generation)

---

## Status

**Alpha (v0.1.0)** - Requires Python 3.10+

- ✅ Core chaos injection
- ✅ LangChain helpers
- ✅ Pre-built scenarios (timeouts, rate limits, auth, content moderation)
- ✅ Observer metrics
- 📦 PyPI publishing soon

---

## Contributing

Contributions welcome! Open an issue or PR.

## License

MIT
