from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from .config import settings

engine = create_async_engine(
    settings.db_url,
    echo=settings.DEBUG,
    poolclass=NullPool,
    connect_args={"check_same_thread": False} if settings.is_sqlite else {},
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    from .models.user import User
    from .models.destination import Destination
    from .models.hotel import Hotel
    from .models.food import FoodItem
    from .models.trip import Trip, TripDay, TripActivity
    from .models.review import Review
    from .models.favorite import Favorite
    from .models.chat import ChatMessage
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with engine.begin() as conn:
        def add_missing_columns(sync_conn):
            from sqlalchemy import inspect, text
            inspector = inspect(sync_conn)
            columns = [c["name"] for c in inspector.get_columns("users")]
            if "reset_token" not in columns:
                sync_conn.execute(text("ALTER TABLE users ADD COLUMN reset_token VARCHAR(255)"))
            if "reset_token_expiry" not in columns:
                sync_conn.execute(text("ALTER TABLE users ADD COLUMN reset_token_expiry TIMESTAMP"))
        try:
            await conn.run_sync(add_missing_columns)
        except Exception:
            pass
