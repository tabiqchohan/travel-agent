from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from ..models.hotel import HotelCategory


class HotelCreate(BaseModel):
    destination_id: str
    name: str
    description: Optional[str] = None
    category: HotelCategory
    price_per_night: Optional[float] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    amenities: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class HotelResponse(BaseModel):
    id: str
    destination_id: str
    name: str
    description: Optional[str] = None
    category: HotelCategory
    price_per_night: Optional[float] = None
    rating: float
    address: Optional[str] = None
    image_url: Optional[str] = None
    amenities: Optional[str] = None
    contact_phone: Optional[str] = None
    website: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    is_active: bool
    created_at: datetime
    currency: str = "USD"

    class Config:
        from_attributes = True


class HotelSearch(BaseModel):
    destination: str
    category: Optional[HotelCategory] = None
    max_price: Optional[float] = None
