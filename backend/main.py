from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import init_db
from .routers import auth, destinations, hotels, food, trips, budget, weather, smart, reviews, favorites
from .utils.seed_data import seed_destinations
from .database import async_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as db:
        await seed_destinations(db)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Advanced Travel Agent API with destination, hotel, food recommendations, trip planning, budget estimation, and more.",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_prefix = "/v1"

app.include_router(auth.router, prefix=api_prefix)
app.include_router(destinations.router, prefix=api_prefix)
app.include_router(hotels.router, prefix=api_prefix)
app.include_router(food.router, prefix=api_prefix)
app.include_router(trips.router, prefix=api_prefix)
app.include_router(budget.router, prefix=api_prefix)
app.include_router(weather.router, prefix=api_prefix)
app.include_router(smart.router, prefix=api_prefix)
app.include_router(reviews.router, prefix=api_prefix)
app.include_router(favorites.router, prefix=api_prefix)


@app.get("/v1/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
