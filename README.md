# 🐒 Tool Monkey

<img src="./images/monkey.png">

> Chaos testing for LLM agents. Inspired by Netflix's Chaos Monkey, built for the agentic era.

## Quick Start

```python
from tool_monkey import with_monkey, FailureScenario, ToolFailure

# Define what should fail
scenario = FailureScenario(
    name="api_timeout",
    failures=[ToolFailure(tool_name="fetch_api", on_call_count=1, error_type="timeout")]
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

Modern generative AI and agentic workflows rely on tool calls (APIs, functions, external services) that can fail in unpredictable ways. Tool Monkey provides a deterministic way to inject failures—timeouts, exceptions, malformed outputs—into tool calls so that application retry, fallback and error handling logic can be tested reliably

## Features

- **Framework-agnostic** - Works with LangGraph, LangChain, AutoGen, or custom runtimes
- **Deterministic chaos** - Same scenario = same failures
- **Observable** - Track success rates, retries, latency, and costs
- **Pre-built scenarios** - Rate limits, timeouts, auth failures, and more

## Installation

```bash
pip install tool-monkey  # Coming soon
```

For now:

```bash
git clone https://github.com/yourusername/tool-monkey
cd tool-monkey
pip install -e .
```

## Status

**Early development** - Building V1. Contributions welcome!
