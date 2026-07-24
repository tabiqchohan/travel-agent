from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from ..models.destination import Destination
from ..models.food import FoodItem, FoodCategory
from ..schemas.food import FoodCreate, FoodResponse, FoodSearch


class FoodService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, params: FoodSearch) -> list[FoodResponse]:
        dest_result = await self.db.execute(
            select(Destination).where(
                Destination.is_active == True,
                Destination.name.ilike(f"%{params.destination}%")
            )
        )
        destination = dest_result.scalar_one_or_none()
        if not destination:
            return []

        query = select(FoodItem).where(
            FoodItem.destination_id == destination.id,
            FoodItem.is_active == True,
        )
        if params.category:
            query = query.where(FoodItem.category == params.category)
        if params.vegetarian is not None:
            query = query.where(FoodItem.is_vegetarian == params.vegetarian)

        query = query.order_by(FoodItem.name)
        result = await self.db.execute(query)
        return [FoodResponse.model_validate(f) for f in result.scalars().all()]

    async def get_by_destination_name(self, destination_name: str) -> list[FoodResponse]:
        dest_result = await self.db.execute(
            select(Destination).where(
                Destination.is_active == True,
                Destination.name.ilike(f"%{destination_name}%")
            )
        )
        destination = dest_result.scalar_one_or_none()
        if not destination:
            return []

        result = await self.db.execute(
            select(FoodItem).where(
                FoodItem.destination_id == destination.id,
                FoodItem.is_active == True,
            ).order_by(FoodItem.category, FoodItem.name)
        )
        return [FoodResponse.model_validate(f) for f in result.scalars().all()]

    async def create(self, data: FoodCreate) -> FoodResponse:
        food = FoodItem(**data.model_dump())
        self.db.add(food)
        await self.db.flush()
        return FoodResponse.model_validate(food)
