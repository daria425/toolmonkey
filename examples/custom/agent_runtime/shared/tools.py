from typing import Union, Optional
import os
import random
from dotenv import load_dotenv
from agent_runtime.shared.models import FetchedLogs, FetchedEnvVar, FetchedGoogleShopResults, GoogleShopItem
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


def fetch_related_queries(query: str):
    num_items = 3
    product_templates = [
        {"name": "Wireless Bluetooth Headphones",
            "price": "$79.99", "rating": 4.5, "vendor": "TechGear"},
        {"name": "Premium Running Shoes", "price": "$129.99",
            "rating": 4.8, "vendor": "SportsPro"},
        {"name": "Stainless Steel Water Bottle",
            "price": "$24.99", "rating": 4.6, "vendor": "EcoLife"},
        {"name": "Smart Fitness Watch", "price": "$199.99",
            "rating": 4.7, "vendor": "FitTech"},
        {"name": "Portable Phone Charger", "price": "$34.99",
            "rating": 4.4, "vendor": "PowerMax"},
        {"name": "Ergonomic Laptop Stand", "price": "$49.99",
            "rating": 4.9, "vendor": "DeskPro"},
        {"name": "Noise Cancelling Earbuds", "price": "$89.99",
            "rating": 4.3, "vendor": "AudioPlus"},
        {"name": "Yoga Mat with Carry Strap", "price": "$39.99",
            "rating": 4.7, "vendor": "FitLife"},
        {"name": "LED Desk Lamp", "price": "$45.99",
            "rating": 4.5, "vendor": "BrightHome"},
        {"name": "Insulated Travel Mug", "price": "$29.99",
            "rating": 4.6, "vendor": "TravelEase"}
    ]
    selected_items = random.sample(product_templates, num_items)
    items = [GoogleShopItem(**item) for item in selected_items]

    logger.info(
        f"Fetched {len(items)}")

    return FetchedGoogleShopResults(
        items=items
    )
