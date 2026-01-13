from tool_monkey import ToolFailure, FailureScenario


def burst_rate_limit(on_call: int = 3, retry_after: float = 5.0) -> FailureScenario:
    return FailureScenario(
        name="burst_rate_limit",
        failures=[
            ToolFailure(
                error_type="rate_limit",
                on_call_count=on_call,
                config={
                    "rate_limit": {
                        "retry_after": retry_after,
                        "limit_type": "burst",
                        "remaining": 0
                    }
                }
            )
        ]
    )
