from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):

    database_url: str
    poll_interval: int = 5
    storage_root: Path = BASE_DIR / "storage" / "repositories"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()