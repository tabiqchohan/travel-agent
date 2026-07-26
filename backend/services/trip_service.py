from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from ..models.trip import Trip, TripDay, TripActivity, TripStatus
from ..schemas.trip import TripCreate, TripUpdate, TripResponse, TripDayCreate, TripActivityCreate


class TripService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id: str, data: TripCreate) -> TripResponse:
        trip = Trip(
            user_id=user_id,
            title=data.title,
            description=data.description,
            destination_id=data.destination_id,
            start_date=data.start_date,
            end_date=data.end_date,
            budget_total=data.budget_total,
            is_public=data.is_public,
        )
        self.db.add(trip)
        await self.db.flush()

        for day_data in data.days:
            day = TripDay(
                trip_id=trip.id,
                day_number=day_data.day_number,
                date=day_data.date,
                notes=day_data.notes,
            )
            self.db.add(day)
            await self.db.flush()

            for act_data in day_data.activities:
                activity = TripActivity(
                    trip_day_id=day.id,
                    **act_data.model_dump(),
                )
                self.db.add(activity)

        await self.db.flush()
        return await self.get_by_id(trip.id)

    async def get_by_id(self, trip_id: str) -> Optional[TripResponse]:
        result = await self.db.execute(select(Trip).where(Trip.id == trip_id))
        trip = result.scalar_one_or_none()
        return await self._load_relations(trip) if trip else None

    async def get_user_trips(self, user_id: str) -> list[TripResponse]:
        result = await self.db.execute(
            select(Trip).where(Trip.user_id == user_id).order_by(Trip.updated_at.desc())
        )
        trips = result.scalars().all()
        return [await self._load_relations(t) for t in trips]

    async def update(self, trip_id: str, user_id: str, data: TripUpdate) -> Optional[TripResponse]:
        result = await self.db.execute(select(Trip).where(Trip.id == trip_id, Trip.user_id == user_id))
        trip = result.scalar_one_or_none()
        if not trip:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(trip, key, value)

        await self.db.flush()
        return await self._load_relations(trip)

    async def delete(self, trip_id: str, user_id: str) -> bool:
        result = await self.db.execute(select(Trip).where(Trip.id == trip_id, Trip.user_id == user_id))
        trip = result.scalar_one_or_none()
        if not trip:
            return False
        await self.db.delete(trip)
        await self.db.flush()
        return True

    async def _load_relations(self, trip: Trip) -> TripResponse:
        from ..schemas.trip import TripDayResponse, TripActivityResponse

        days_result = await self.db.execute(
            select(TripDay).where(TripDay.trip_id == trip.id).order_by(TripDay.day_number)
        )
        days = days_result.scalars().all()

        trip_data = {
            "id": trip.id,
            "user_id": trip.user_id,
            "title": trip.title,
            "description": trip.description,
            "destination_id": trip.destination_id,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "budget_total": trip.budget_total,
            "status": trip.status,
            "is_public": trip.is_public,
            "created_at": trip.created_at,
            "updated_at": trip.updated_at,
            "days": [],
        }

        for day in days:
            acts_result = await self.db.execute(
                select(TripActivity).where(TripActivity.trip_day_id == day.id).order_by(TripActivity.start_time)
            )
            activities = acts_result.scalars().all()

            trip_data["days"].append(TripDayResponse(
                id=day.id,
                trip_id=day.trip_id,
                day_number=day.day_number,
                date=day.date,
                notes=day.notes,
                activities=[TripActivityResponse.model_validate(a) for a in activities],
            ))

        return TripResponse(**trip_data)
