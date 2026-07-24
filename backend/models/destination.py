import uuid
from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, Enum, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..database import Base


class TravelInterest(str, enum.Enum):
    BEACH = "beach"
    CULTURE = "culture"
    ADVENTURE = "adventure"
    FOOD = "food"
    GENERAL = "general"


class BudgetLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TravelType(str, enum.Enum):
    FAMILY = "family"
    ROMANTIC = "romantic"
    SOLO = "solo"
    BUSINESS = "business"
    GENERAL = "general"


class Destination(Base):
    __tablename__ = "destinations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), index=True)
    country: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    interest: Mapped[TravelInterest] = mapped_column(Enum(TravelInterest))
    budget_level: Mapped[BudgetLevel] = mapped_column(Enum(BudgetLevel))
    travel_type: Mapped[TravelType] = mapped_column(Enum(TravelType), default=TravelType.GENERAL)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    best_time_to_visit: Mapped[str] = mapped_column(String(200), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=True)
    timezone: Mapped[str] = mapped_column(String(50), nullable=True)
    lat: Mapped[float] = mapped_column(Float, nullable=True)
    lng: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    hotels = relationship("Hotel", back_populates="destination", cascade="all, delete-orphan")
    food_items = relationship("FoodItem", back_populates="destination", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="destination", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="destination", cascade="all, delete-orphan")
