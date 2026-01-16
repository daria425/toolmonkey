
from pydantic import BaseModel


class WeatherToolInput(BaseModel):
    location: str
    units: str = "celsius"


def base_weather_tool(location: str, units: str = "celsius"):
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    return result


def base_image_gen_tool(prompt: str, style: str):
    """
    Generate an image using AI (mock DALL-E, Midjourney, etc.)

    These APIs have STRICT rate limits:
    - Free tier: 5 images/minute
    - Agents asking for multiple variations would hit this fast
    """
    return {
        "image_url": f"https://fake-cdn.com/images/{hash(prompt)}.png",
        "prompt": prompt,
        "style": style,
        "generation_time": 2.3
    }
