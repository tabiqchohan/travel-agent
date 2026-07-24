from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ..models.favorite import FavoriteType
from .destination import DestinationResponse


class FavoriteCreate(BaseModel):
    favorite_type: FavoriteType
    destination_id: Optional[str] = None
    hotel_id: Optional[str] = None
    food_item_id: Optional[str] = None
    notes: Optional[str] = None


class FavoriteResponse(BaseModel):
    id: str
    user_id: str
    favorite_type: FavoriteType
    destination_id: Optional[str] = None
    hotel_id: Optional[str] = None
    food_item_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    destination: Optional[DestinationResponse] = None

    class Config:
        from_attributes = True
