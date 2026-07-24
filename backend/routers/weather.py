from fastapi import APIRouter, Query
from typing import Optional

from ..schemas.weather import WeatherResponse
from ..services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("", response_model=WeatherResponse)
async def get_weather(
    destination: str,
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
):
    service = WeatherService()
    return await service.get_weather(destination, lat, lng)
