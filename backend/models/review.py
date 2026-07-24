import uuid
from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, Enum, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..database import Base


class ReviewType(str, enum.Enum):
    DESTINATION = "destination"
    HOTEL = "hotel"
    FOOD = "food"


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    review_type: Mapped[ReviewType] = mapped_column(Enum(ReviewType))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=True)
    hotel_id: Mapped[str] = mapped_column(String(36), ForeignKey("hotels.id"), nullable=True)
    food_item_id: Mapped[str] = mapped_column(String(36), ForeignKey("food_items.id"), nullable=True)
    rating: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(200), nullable=True)
    content: Mapped[str] = mapped_column(Text)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="reviews")
    destination = relationship("Destination", back_populates="reviews")
