import uuid
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..database import Base


class FavoriteType(str, enum.Enum):
    DESTINATION = "destination"
    HOTEL = "hotel"
    FOOD = "food"


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (
        UniqueConstraint("user_id", "destination_id", "favorite_type", name="uq_user_favorite"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    favorite_type: Mapped[FavoriteType] = mapped_column(Enum(FavoriteType))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=True)
    hotel_id: Mapped[str] = mapped_column(String(36), ForeignKey("hotels.id"), nullable=True)
    food_item_id: Mapped[str] = mapped_column(String(36), ForeignKey("food_items.id"), nullable=True)
    notes: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="favorites")
    destination = relationship("Destination", back_populates="favorites")
