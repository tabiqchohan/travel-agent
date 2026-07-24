from typing import Optional
from pydantic import BaseModel


class WeatherResponse(BaseModel):
    destination: str
    temperature_c: float
    feels_like_c: float
    humidity: int
    description: str
    icon: str
    wind_speed: float
    forecast: list[dict] = []
