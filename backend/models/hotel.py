import uuid
from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, Enum, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..database import Base


class HotelCategory(str, enum.Enum):
    BUDGET = "budget"
    MID_RANGE = "mid_range"
    LUXURY = "luxury"


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"))
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[HotelCategory] = mapped_column(Enum(HotelCategory))
    price_per_night: Mapped[float] = mapped_column(Float, nullable=True)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    amenities: Mapped[str] = mapped_column(Text, nullable=True)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    website: Mapped[str] = mapped_column(String(500), nullable=True)
    lat: Mapped[float] = mapped_column(Float, nullable=True)
    lng: Mapped[float] = mapped_column(Float, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    destination = relationship("Destination", back_populates="hotels")
