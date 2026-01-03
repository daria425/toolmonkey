from typing import Union, Optional
import os
from dotenv import load_dotenv
from agent_runtime.shared.models import FetchedLogs, FetchedEnvVar
from agent_runtime.shared.utils.logger import logger


def fetch_logs(reasoning: str, confidence: Union[int, float], num_lines: Optional[int] = None, log_file_path: Optional[str] = None):
    print(log_file_path)
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
