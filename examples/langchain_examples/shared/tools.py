
from pydantic import BaseModel


class WeatherToolInput(BaseModel):
    location: str
    units: str = "celsius"


def base_weather_tool(location: str, units: str = "celsius"):
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    return result
