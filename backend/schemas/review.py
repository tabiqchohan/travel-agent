from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from ..models.review import ReviewType


class ReviewCreate(BaseModel):
    review_type: ReviewType
    destination_id: Optional[str] = None
    hotel_id: Optional[str] = None
    food_item_id: Optional[str] = None
    rating: int = Field(ge=1, le=5)
    title: Optional[str] = None
    content: str


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    review_type: ReviewType
    destination_id: Optional[str] = None
    hotel_id: Optional[str] = None
    food_item_id: Optional[str] = None
    rating: int
    title: Optional[str] = None
    content: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
