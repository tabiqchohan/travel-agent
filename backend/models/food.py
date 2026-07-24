import uuid
from datetime import datetime
from sqlalchemy import String, Text, Float, Enum, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from ..database import Base


class FoodCategory(str, enum.Enum):
    STREET_FOOD = "street_food"
    MAIN_DISH = "main_dish"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SNACK = "snack"


class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"))
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[FoodCategory] = mapped_column(Enum(FoodCategory), nullable=True)
    price_range: Mapped[str] = mapped_column(String(50), nullable=True)
    is_vegetarian: Mapped[bool] = mapped_column(Boolean, default=False)
    is_vegan: Mapped[bool] = mapped_column(Boolean, default=False)
    spice_level: Mapped[str] = mapped_column(String(20), nullable=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    destination = relationship("Destination", back_populates="food_items")
