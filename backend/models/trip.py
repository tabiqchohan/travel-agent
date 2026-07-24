import uuid
from datetime import datetime, date
from sqlalchemy import String, Text, Float, Integer, Date, DateTime, func, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..database import Base


class TripStatus(str, enum.Enum):
    DRAFT = "draft"
    PLANNING = "planning"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=True)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    budget_total: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[TripStatus] = mapped_column(SAEnum(TripStatus), default=TripStatus.DRAFT)
    is_public: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="trips")
    days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan", order_by="TripDay.day_number")


class TripDay(Base):
    __tablename__ = "trip_days"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id: Mapped[str] = mapped_column(String(36), ForeignKey("trips.id"))
    day_number: Mapped[int] = mapped_column(Integer)
    date: Mapped[date] = mapped_column(Date, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    trip = relationship("Trip", back_populates="days")
    activities = relationship("TripActivity", back_populates="trip_day", cascade="all, delete-orphan", order_by="TripActivity.start_time")


class TripActivity(Base):
    __tablename__ = "trip_activities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_day_id: Mapped[str] = mapped_column(String(36), ForeignKey("trip_days.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_time: Mapped[str] = mapped_column(String(10), nullable=True)
    end_time: Mapped[str] = mapped_column(String(10), nullable=True)
    location: Mapped[str] = mapped_column(String(200), nullable=True)
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    category: Mapped[str] = mapped_column(String(50), nullable=True)
    booking_url: Mapped[str] = mapped_column(String(500), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    trip_day = relationship("TripDay", back_populates="activities")
