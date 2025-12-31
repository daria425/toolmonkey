# 🐒 Tool Monkey

> Chaos testing for LLM agents. Inspired by Netflix's Chaos Monkey, built for the agentic era.

**Tool Monkey** is my take in a chaos testing toolkit for LLM-based agents.

Most agent frameworks hide their error handling deep in abstractions so I am building Tool Monkey to:

- **Inject failures** at the tool boundary (rate limits, timeouts, malformed data)
- **Test robustness** with reproducible failure scenarios
- **Observe behavior** when things go wrong
- **Build confidence** before production deployment

## Why does this exist?

Production agents fail in ways you can't predict:

- APIs rate limit mid-conversation
- Auth tokens expire
- Tools return partial or malformed data
- Network timeouts break multi-step workflows

There's no good way to test these scenarios systematically. Tool Monkey makes failure testing **deterministic and reproducible** - critical for CI/CD and agent reliability.

## The approach

Tool Monkey provides:

1. **Minimal agent runtime** - Clean, observable execution for testing
2. **Chaos scenarios** - Declarative failure definitions (rate limits, timeouts, auth errors)
3. **Tool injection layer** - Failures injected only at tool execution
4. **Observability** - Full execution traces, metrics, and logs

Failures never affect agent prompts or LLM responses - only tool calls. This keeps tests focused and reproducible.
