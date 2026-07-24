from typing import Optional
import httpx

from ..config import settings
from ..schemas.weather import WeatherResponse


class WeatherService:
    async def get_weather(self, destination: str, lat: Optional[float] = None, lng: Optional[float] = None) -> Optional[WeatherResponse]:
        if not settings.OPENWEATHER_API_KEY:
            return self._get_demo_weather(destination)

        try:
            if lat and lng:
                url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
            else:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={destination}&appid={settings.OPENWEATHER_API_KEY}&units=metric"

            async with httpx.AsyncClient() as client:
                resp = await client.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    return WeatherResponse(
                        destination=destination,
                        temperature_c=data["main"]["temp"],
                        feels_like_c=data["main"]["feels_like"],
                        humidity=data["main"]["humidity"],
                        description=data["weather"][0]["description"],
                        icon=data["weather"][0]["icon"],
                        wind_speed=data["wind"]["speed"],
                    )
        except Exception:
            pass

        return self._get_demo_weather(destination)

    def _get_demo_weather(self, destination: str) -> WeatherResponse:
        import random
        temp = round(random.uniform(20, 35), 1)
        conditions = ["Clear sky", "Partly cloudy", "Sunny", "Light breeze", "Few clouds"]
        return WeatherResponse(
            destination=destination,
            temperature_c=temp,
            feels_like_c=round(temp + random.uniform(-2, 2), 1),
            humidity=random.randint(50, 85),
            description=random.choice(conditions),
            icon="01d",
            wind_speed=round(random.uniform(5, 25), 1),
        )
