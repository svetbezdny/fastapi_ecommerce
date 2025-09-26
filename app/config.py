from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    BASE_PATH: Path = Path(__file__).parent

    TITLE: str = "FastAPI Online Store"
    VERSION: str = "0.1.0"

    HOST: str = "localhost"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"

    DATABASE_URL: str = "sqlite:///ecommerce.db"
    ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=(BASE_PATH.parent / ".env").resolve(),
        extra="ignore",
    )


settings = Settings()
