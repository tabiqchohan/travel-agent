from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from ..models.destination import Destination
from ..models.hotel import Hotel, HotelCategory
from ..schemas.hotel import HotelCreate, HotelResponse, HotelSearch


class HotelService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search(self, params: HotelSearch) -> list[HotelResponse]:
        dest_result = await self.db.execute(
            select(Destination).where(
                Destination.is_active == True,
                Destination.name.ilike(f"%{params.destination}%")
            )
        )
        destination = dest_result.scalar_one_or_none()
        if not destination:
            return []

        query = select(Hotel).where(
            Hotel.destination_id == destination.id,
            Hotel.is_active == True,
        )
        if params.category:
            query = query.where(Hotel.category == params.category)
        if params.max_price:
            query = query.where(Hotel.price_per_night <= params.max_price)

        query = query.order_by(Hotel.rating.desc())
        result = await self.db.execute(query)
        return [HotelResponse.model_validate(h) for h in result.scalars().all()]

    async def get_by_destination_name(self, destination_name: str) -> list[HotelResponse]:
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
            select(Hotel).where(
                Hotel.destination_id == destination.id,
                Hotel.is_active == True,
            ).order_by(Hotel.category, Hotel.price_per_night)
        )
        return [HotelResponse.model_validate(h) for h in result.scalars().all()]

    async def create(self, data: HotelCreate) -> HotelResponse:
        hotel = Hotel(**data.model_dump())
        self.db.add(hotel)
        await self.db.flush()
        return HotelResponse.model_validate(hotel)
