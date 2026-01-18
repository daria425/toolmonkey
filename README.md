# 🐒 Tool Monkey

![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)

<img src="./images/monkey.png">

> Chaos testing for LLM agents. Inspired by Netflix's Chaos Monkey, built for the agentic era.

## Quick Start

```python
from tool_monkey import with_monkey, FailureScenario, ToolFailure

# Define what should fail
scenario = FailureScenario(
    name="api_timeout",
    failures=[ToolFailure(on_call_count=1, error_type="timeout")]
)

# Decorate your tool
@with_monkey(scenario)
def fetch_api(url: str):
    return requests.get(url).json()

# First call fails, second succeeds
fetch_api("https://api.example.com")  # ← TimeoutError
fetch_api("https://api.example.com")  # ← Works
```

## What is it and why?

Tool Monkey is an experimental Python library for chaos testing LLM agent tool calls.

Modern generative AI and agentic workflows rely on tool calls (APIs, functions, external services) that can fail in unpredictable ways. Tool Monkey provides a deterministic way to inject failures (timeouts, exceptions, malformed outputs) into tool calls so that application retry, fallback and error handling logic can be tested reliably.

## Why Tool Monkey?

LLM agents call APIs that fail. A lot. But testing and implementing error handling without real failures is hard:

- **Expensive**: Triggering real rate limits costs API credits
- **Slow**: Waiting for actual timeouts wastes development time
- **Unpredictable**: Can't reproduce exact failure scenarios reliably
- **Risky**: Hard to test auth failures without revoking real credentials

Tool Monkey lets you test and build error handling in your agentic workflows without actually encountering authentication failures, rate limits, timeouts, or other real API errors.

## Features

- **Built for LangChain** - Drop-in decorator for LangChain tools (works with any Python function)
- **Deterministic chaos** - Same scenario = same failures, every time
- **Observable** - Track success rates, retries, latency with built-in metrics
- **Pre-built scenarios** - Timeouts, rate limits, auth failures, and more
- **Easy integration** - Works with `bind_tools()`, tenacity retry, and LangGraph

## Installation

```bash
pip install tool-monkey  # Not published yet, see below
```

For now (install from source):

```bash
git clone https://github.com/daria425/tool-monkey
cd tool-monkey
pip install -e .
```

## LangChain Example

```python
from langchain_core.tools import tool
from tool_monkey import with_monkey, burst_rate_limit, MonkeyObserver
from tenacity import retry, stop_after_attempt, wait_exponential

# Create chaos scenario
observer = MonkeyObserver()
scenario = burst_rate_limit(on_call=3, retry_after=5.0)

# Base tool function
def base_search_api(query: str):
    return f"Results for {query}"

# Wrap with chaos
wrapped_tool = with_monkey(scenario, observer)(base_search_api)

# Add retry logic
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
def search_with_retry(query: str):
    return wrapped_tool(query)

# Create LangChain tool
@tool
def search_tool(query: str):
    """Search the web for information."""
    return search_with_retry(query)

# Use with your agent
llm_with_tools = llm.bind_tools([search_tool])
# Agent will hit rate limit on 3rd call, retry logic kicks in
```

## Status

**Alpha (v0.1.0)** - Ready for testing. Requires Python 3.10+

- ✅ **Core**: Chaos injection, observer metrics, scenario framework
- ✅ **Scenarios**: Timeouts, rate limits, auth failures
- ✅ **Examples**: LangChain notebooks with real retry patterns
- 📦 **PyPI**: Publishing soon

Contributions welcome!
