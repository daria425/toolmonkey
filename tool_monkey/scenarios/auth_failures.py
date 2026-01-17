from tool_monkey import ToolFailure, FailureScenario


def expired_token(on_call: int = 3) -> FailureScenario:
    """
    Token expires mid-session (401 Unauthorized).

    Realistic: OAuth tokens expire after 1 hour. Agent running for 2 hours hits this.
    """
    return FailureScenario(
        name="expired_token",
        failures=[
            ToolFailure(
                on_call_count=on_call,
                error_type="auth_failure",
                config={
                    "auth_failure": {
                        "failure_type": "unauthorized",
                        "status_code": 401,
                        "error_message": "Access token expired"
                    }
                }
            )
        ]
    )


def forbidden_access() -> FailureScenario:
    """403 Forbidden - no permission to access resource."""
    return FailureScenario(
        name="forbidden_access",
        failures=[
            ToolFailure(
                on_call_count=1,
                error_type="auth_failure",
                config={
                    "auth_failure": {
                        "failure_type": "forbidden",
                        "status_code": 403,
                        "error_message": "Insufficient permissions"
                    }
                }
            )
        ]
    )


def invalid_api_key() -> FailureScenario:
    """Invalid/revoked API key."""
    return FailureScenario(
        name="invalid_api_key",
        failures=[
            ToolFailure(
                on_call_count=1,
                error_type="auth_failure",
                config={
                    "auth_failure": {
                        "failure_type": "invalid_key",
                        "status_code": 401,
                        "error_message": "Invalid API key"
                    }
                }
            )
        ]
    )
