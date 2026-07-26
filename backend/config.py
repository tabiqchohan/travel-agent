import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Travel Agent Pro"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./travel_agent.db"
    DATABASE_URL_POSTGRES: str = ""

    @property
    def db_url(self) -> str:
        from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
        url = self.DATABASE_URL_POSTGRES or self.DATABASE_URL
        if "postgresql" in url and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://")
        parsed = urlparse(url)
        if parsed.query:
            params = parse_qs(parsed.query)
            for key in ["sslmode", "channel_binding"]:
                params.pop(key, None)
            query = urlencode(params, doseq=True)
            url = urlunparse(parsed._replace(query=query))
        return url

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.db_url

    SECRET_KEY: str = "change-this-to-a-secure-random-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    OPENWEATHER_API_KEY: str = ""
    EXCHANGERATE_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GOOGLE_MAPS_API_KEY: str = ""

    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
