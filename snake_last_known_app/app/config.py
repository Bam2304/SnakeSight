from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./snake.db"
    H3_RESOLUTION: int = 8
    DEFAULT_RADIUS_KM: float = 10.0
    DEFAULT_SINCE_DAYS: int = 90

    class Config:
        env_file = ".env"

settings = Settings()
