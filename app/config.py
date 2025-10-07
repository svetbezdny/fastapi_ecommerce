from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).parent

    TITLE: str = "FastAPI Online Store"
    VERSION: str = "0.1.0"

    HOST: str = "localhost"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"

    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SQLITE_DATABASE_URL: str = "sqlite:///ecommerce.db"
    ECHO: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=(BASE_PATH.parent / ".env").resolve(),
        extra="ignore",
    )


settings = Settings()  # type: ignore
