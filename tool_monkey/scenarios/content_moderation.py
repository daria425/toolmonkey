from tool_monkey import ToolFailure, FailureScenario


def content_policy_violation(reason: str = "nsfw_content") -> FailureScenario:
    """Image gen / LLM API rejects prompt for policy violation

      Examples:
      - "Your prompt contains prohibited content"
      - "Content policy violation: violence detected"
      - OpenAI content filter triggered
      """
    content_categories = {
        reason: True,
    }
    return FailureScenario(
        name="content_policy_violation",
        failures=[
            ToolFailure(
                error_type="content_moderation",
                on_call_count=1,
                config={
                    "content_moderation": {
                        "content_categories": content_categories,
                        "reason": reason
                    }
                }
            )
        ]
    )
