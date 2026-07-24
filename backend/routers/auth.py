from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse, UserUpdate
from ..services.auth_service import AuthService
from ..utils.security import get_current_user
from ..models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(data)


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_profile(data: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.update_profile(current_user.id, data)
