from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from ..models.destination import TravelInterest, BudgetLevel, TravelType


class DestinationCreate(BaseModel):
    name: str
    country: str
    description: str
    image_url: Optional[str] = None
    interest: TravelInterest
    budget_level: BudgetLevel
    travel_type: TravelType = TravelType.GENERAL
    best_time_to_visit: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class DestinationResponse(BaseModel):
    id: str
    name: str
    country: str
    description: str
    image_url: Optional[str] = None
    interest: TravelInterest
    budget_level: BudgetLevel
    travel_type: TravelType
    rating: float
    best_time_to_visit: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class DestinationSearch(BaseModel):
    travel_type: Optional[TravelType] = None
    budget: Optional[BudgetLevel] = None
    interest: Optional[TravelInterest] = None
    query: Optional[str] = None
