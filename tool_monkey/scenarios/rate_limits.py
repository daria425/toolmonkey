from tool_monkey import ToolFailure, FailureScenario


def burst_rate_limit(on_call: int = 3, retry_after: float = 5.0) -> FailureScenario:
    """
      Simulate hitting a burst rate limit on the Nth call.

      Common scenario: API allows a few rapid requests, then rate limits.
      Example: OpenAI allows ~3 requests/sec, the 3rd rapid request gets 429'd.

      Args:
          on_call: Which call number triggers the rate limit (default: 3)
          retry_after: How many seconds to wait before retrying (default: 5.0)

      Returns:
          FailureScenario configured for burst rate limiting
    """
    return FailureScenario(
        name="burst_rate_limit",
        failures=[
            ToolFailure(
                error_type="rate_limit",
                on_call_count=on_call,
                config={
                    "rate_limit": {
                        "retry_after_seconds": retry_after,
                        "limit_type": "burst",
                        "remaining": 0
                    }
                }
            )
        ]
    )


def progressive_rate_limit(quota: int = 5, retry_after: float = 60.0) -> FailureScenario:
    """
      First N (quota) calls succeed, then ALL subsequent calls fail with rate limit.

      Simulates: You've exhausted your quota (e.g., 100 calls/hour).
      Unlike burst_rate_limit (single failure), this keeps failing until quota resets.

      Example: An API gives you 100 requests/hour. After 100, every call fails 
      until the hour resets.
    """
    return FailureScenario(
        name="progressive_rate_limit",
        failures=[
            ToolFailure(
                on_call_count=i,
                error_type="rate_limit",
                config={
                    "retry_after_seconds": retry_after,
                    "limit_type": "per_minute",
                    "remaining": 0
                }
            )
            for i in range(quota + 1, quota + 20)
        ]
    )
