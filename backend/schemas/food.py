from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from ..models.food import FoodCategory


class FoodCreate(BaseModel):
    destination_id: str
    name: str
    description: Optional[str] = None
    category: Optional[FoodCategory] = None
    price_range: Optional[str] = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    spice_level: Optional[str] = None
    image_url: Optional[str] = None


class FoodResponse(BaseModel):
    id: str
    destination_id: str
    name: str
    description: Optional[str] = None
    category: Optional[FoodCategory] = None
    price_range: Optional[str] = None
    is_vegetarian: bool
    is_vegan: bool
    spice_level: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class FoodSearch(BaseModel):
    destination: str
    category: Optional[FoodCategory] = None
    vegetarian: Optional[bool] = None
