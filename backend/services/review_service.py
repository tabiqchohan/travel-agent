from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List

from ..models.review import Review, ReviewType
from ..models.destination import Destination
from ..schemas.review import ReviewCreate, ReviewResponse


class ReviewService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: str, data: ReviewCreate) -> ReviewResponse:
        review = Review(
            user_id=user_id,
            **data.model_dump(),
        )
        self.db.add(review)
        await self.db.flush()

        if data.review_type == ReviewType.DESTINATION and data.destination_id:
            result = await self.db.execute(
                select(func.avg(Review.rating)).where(
                    Review.destination_id == data.destination_id,
                    Review.review_type == ReviewType.DESTINATION,
                )
            )
            avg_rating = result.scalar() or 0.0
            result2 = await self.db.execute(
                select(Destination).where(Destination.id == data.destination_id)
            )
            dest = result2.scalar_one_or_none()
            if dest:
                dest.rating = round(float(avg_rating), 1)

        await self.db.flush()
        return ReviewResponse.model_validate(review)

    async def get_by_destination(self, destination_id: str) -> list[ReviewResponse]:
        result = await self.db.execute(
            select(Review).where(
                Review.destination_id == destination_id,
                Review.review_type == ReviewType.DESTINATION,
            ).order_by(Review.created_at.desc())
        )
        return [ReviewResponse.model_validate(r) for r in result.scalars().all()]

    async def get_by_user(self, user_id: str) -> list[ReviewResponse]:
        result = await self.db.execute(
            select(Review).where(Review.user_id == user_id).order_by(Review.created_at.desc())
        )
        return [ReviewResponse.model_validate(r) for r in result.scalars().all()]
