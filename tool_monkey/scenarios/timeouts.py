from tool_monkey import ToolFailure, FailureScenario


def single_timeout(seconds: float = 3.0) -> FailureScenario:
    """
    First tool call times out after N seconds, rest succeed.

    :param seconds: Timeout duration in seconds
    :type seconds: float
    :return: FailureScenario with single timeout
    :rtype: FailureScenario
    """
    return FailureScenario(
        name="single_timeout",
        failures=[
            ToolFailure(
                error_type="timeout",
                config={"timeout": {"n_seconds": seconds}}
            )
        ]
    )


def retry_exhaustion(num_failures: int = 3, seconds: float = 2.0) -> FailureScenario:
    """
    First N calls timeout consecutively (tests retry limits).

    :param num_failures: Number of consecutive timeout failures
    :type num_failures: int
    :param seconds: Timeout duration in seconds
    :type seconds: float
    :return: FailureScenario with consecutive timeouts
    :rtype: FailureScenario
    """
    return FailureScenario(
        name="retry_exhaustion",
        failures=[
            ToolFailure(
                error_type="timeout",
                config={"timeout": {"n_seconds": seconds}}
            )
            for _ in range(num_failures)
        ]
    )


def intermittent_timeout(num_cycles: int = 3, seconds: float = 2.0) -> FailureScenario:
    """
    Alternates: timeout, success, timeout, success...

    :param num_cycles: Number of timeout/success cycles
    :type num_cycles: int
    :param seconds: Timeout duration in seconds
    :type seconds: float
    :return: FailureScenario with alternating timeouts
    :rtype: FailureScenario
    """
    failures = []
    for i in range(num_cycles):
        # Timeout on odd calls (1, 3, 5...)
        failures.append(
            ToolFailure(
                on_call_count=i * 2 + 1,
                error_type="timeout",
                config={"timeout": {"n_seconds": seconds}}
            )
        )
    return FailureScenario(name="intermittent_timeout", failures=failures)


def progressive_timeout(delays: list[float] = [1.0, 2.0, 5.0, 10.0]) -> FailureScenario:
    """
    Timeouts get progressively longer (service degradation).

    :param delays: List of timeout durations in seconds for each call
    :type delays: list[float]
    :return: FailureScenario with progressive timeouts
    :rtype: FailureScenario
    """
    return FailureScenario(
        name="progressive_timeout",
        failures=[
            ToolFailure(
                error_type="timeout",
                config={"timeout": {"n_seconds": delay}}
            )
            for delay in delays
        ]
    )
