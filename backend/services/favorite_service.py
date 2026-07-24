from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List

from ..models.favorite import Favorite, FavoriteType
from ..schemas.favorite import FavoriteCreate, FavoriteResponse


class FavoriteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, user_id: str, data: FavoriteCreate) -> FavoriteResponse:
        existing = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.destination_id == data.destination_id,
                Favorite.favorite_type == data.favorite_type,
            )
        )
        if existing.scalar_one_or_none():
            fav = existing.scalar_one_or_none()
            return FavoriteResponse.model_validate(fav)

        fav = Favorite(user_id=user_id, **data.model_dump())
        self.db.add(fav)
        await self.db.flush()
        return FavoriteResponse.model_validate(fav)

    async def remove(self, user_id: str, favorite_id: str) -> bool:
        result = await self.db.execute(
            select(Favorite).where(Favorite.id == favorite_id, Favorite.user_id == user_id)
        )
        fav = result.scalar_one_or_none()
        if not fav:
            return False
        await self.db.delete(fav)
        await self.db.flush()
        return True

    async def get_user_favorites(self, user_id: str) -> list[FavoriteResponse]:
        result = await self.db.execute(
            select(Favorite).where(Favorite.user_id == user_id).order_by(Favorite.created_at.desc())
        )
        favorites = result.scalars().all()
        responses = []
        for fav in favorites:
            resp = FavoriteResponse.model_validate(fav)
            if fav.favorite_type == FavoriteType.DESTINATION and fav.destination_id:
                from ..schemas.destination import DestinationResponse
                from ..models.destination import Destination
                dest_result = await self.db.execute(
                    select(Destination).where(Destination.id == fav.destination_id)
                )
                dest = dest_result.scalar_one_or_none()
                if dest:
                    resp.destination = DestinationResponse.model_validate(dest)
            responses.append(resp)
        return responses

    async def is_favorite(self, user_id: str, destination_id: str) -> bool:
        result = await self.db.execute(
            select(Favorite).where(
                Favorite.user_id == user_id,
                Favorite.destination_id == destination_id,
            )
        )
        return result.scalar_one_or_none() is not None
