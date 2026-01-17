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

- **Framework-agnostic** - Works with LangGraph, LangChain, AutoGen, or custom runtimes
- **Deterministic chaos** - Same scenario = same failures
- **Observable** - Track success rates, retries, latency, and costs
- **Pre-built timeout scenarios** - More failure types coming soon (rate limits, auth failures, etc.)

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
