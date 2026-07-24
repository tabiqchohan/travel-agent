from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse, UserUpdate
from ..utils.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, data: UserCreate) -> TokenResponse:
        existing = await self.db.execute(
            select(User).where((User.username == data.username) | (User.email == data.email))
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username or email already registered")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        self.db.add(user)
        await self.db.flush()

        token = create_access_token({"sub": user.id})
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    async def login(self, data: UserLogin) -> TokenResponse:
        result = await self.db.execute(select(User).where(User.username == data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token({"sub": user.id})
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )

    async def get_profile(self, user_id: str) -> UserResponse:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    async def update_profile(self, user_id: str, data: UserUpdate) -> UserResponse:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await self.db.flush()
        return UserResponse.model_validate(user)
