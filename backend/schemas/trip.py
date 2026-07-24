from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field

from ..models.trip import TripStatus


class TripActivityCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    cost: float = 0.0
    category: Optional[str] = None
    booking_url: Optional[str] = None
    notes: Optional[str] = None


class TripActivityResponse(BaseModel):
    id: str
    trip_day_id: str
    title: str
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    cost: float
    category: Optional[str] = None
    booking_url: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class TripDayCreate(BaseModel):
    day_number: int
    date: Optional[date] = None
    notes: Optional[str] = None
    activities: List[TripActivityCreate] = []


class TripDayResponse(BaseModel):
    id: str
    trip_id: str
    day_number: int
    date: Optional[date] = None
    notes: Optional[str] = None
    activities: List[TripActivityResponse] = []

    class Config:
        from_attributes = True


class TripCreate(BaseModel):
    title: str
    description: Optional[str] = None
    destination_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget_total: float = 0.0
    is_public: bool = False
    days: List[TripDayCreate] = []


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    destination_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget_total: Optional[float] = None
    status: Optional[TripStatus] = None
    is_public: Optional[bool] = None


class TripResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    destination_id: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget_total: float
    status: TripStatus
    is_public: bool
    created_at: datetime
    updated_at: datetime
    days: List[TripDayResponse] = []

    class Config:
        from_attributes = True
