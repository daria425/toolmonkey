from typing import Union, Optional
from tool_monkey import with_monkey, ToolFailure, FailureScenario, MonkeyObserver
import os
from dotenv import load_dotenv
from agent_runtime.models import FetchedLogs, FetchedEnvVar
from utils.logger import logger
fetch_logs_failure = FailureScenario(
    name="fetch_logs_timeout",
    failures=[ToolFailure(tool_name="fetch_logs",
                          on_call_count=1, error_type="timeout", config={"timeout": {"n_seconds": 2}}),
              #   ToolFailure(tool_name="fetch_logs",
              #               on_call_count=1, error_type="timeout", config={"timeout": {"n_seconds": 3}}),
              ]
)

observer_instance = MonkeyObserver()


@with_monkey(fetch_logs_failure, observer=observer_instance)
def fetch_logs(reasoning: str, confidence: Union[int, float], num_lines: Optional[int] = None, log_file_path: Optional[str] = None):
    if not os.path.exists(log_file_path):
        raise RuntimeError("Log file path does not exist")
    lines = []
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()
        if num_lines:
            lines = lines[-num_lines:]
    if not lines:
        raise RuntimeError("No logs found")
    logger.info(f"Fetched {len(lines)} log lines from {log_file_path}")
    return FetchedLogs(
        reasoning=reasoning,
        confidence=confidence,
        logs=lines
    )


def fetch_env(env_var: str, reasoning: str, confidence: Union[int, float], mock_env_path: str):
    load_dotenv(dotenv_path=mock_env_path)
    fetched_env_var = os.getenv(env_var, None)
    if not fetched_env_var:
        raise RuntimeError("Environment variable not set")
    logger.info(f"Fetched environment variable {env_var}")
    return FetchedEnvVar(
        env_value=fetched_env_var,
        reasoning=reasoning,
        confidence=confidence
    )
