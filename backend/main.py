from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import init_db, async_session, engine
from .routers import auth, destinations, hotels, food, trips, budget, weather, smart, reviews, favorites, chat
from .utils.seed_data import seed_destinations

_db_initialized = False
_db_error = None


async def ensure_db():
    global _db_initialized, _db_error
    if not _db_initialized:
        try:
            await init_db()
            async with async_session() as db:
                await seed_destinations(db)
            _db_initialized = True
        except Exception as e:
            _db_error = str(e)
            raise


app = FastAPI(
    title=settings.APP_NAME,
    description="Advanced Travel Agent API",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Credentials": "true",
}


@app.middleware("http")
async def cors_and_db_middleware(request: Request, call_next):
    if request.method == "OPTIONS":
        response = JSONResponse(content="ok", status_code=200)
    else:
        if "/debug/" not in request.url.path and "/health" not in request.url.path:
            try:
                await ensure_db()
            except Exception:
                pass
        try:
            response = await call_next(request)
        except Exception as e:
            response = JSONResponse(
                status_code=500,
                content={"detail": f"{type(e).__name__}: {str(e)}"},
            )

    for key, value in CORS_HEADERS.items():
        response.headers[key] = value
    return response


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
app.include_router(chat.router, prefix=api_prefix)


@app.get("/v1/health")
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}


@app.get("/v1/debug/status")
async def debug_status():
    return {
        "db_initialized": _db_initialized,
        "db_error": _db_error,
        "is_sqlite": settings.is_sqlite,
    }
