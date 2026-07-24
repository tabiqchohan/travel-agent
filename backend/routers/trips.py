from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.trip import TripCreate, TripUpdate, TripResponse
from ..services.trip_service import TripService
from ..utils.security import get_current_user
from ..models.user import User

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("", response_model=TripResponse, status_code=201)
async def create_trip(data: TripCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TripService(db)
    return await service.create(current_user.id, data)


@router.get("", response_model=list[TripResponse])
async def list_trips(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TripService(db)
    return await service.get_user_trips(current_user.id)


@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip(trip_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TripService(db)
    trip = await service.get_by_id(trip_id)
    if not trip or trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(trip_id: str, data: TripUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TripService(db)
    trip = await service.update(trip_id, current_user.id, data)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(trip_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TripService(db)
    deleted = await service.delete(trip_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Trip not found")
