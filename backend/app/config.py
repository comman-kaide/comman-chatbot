from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Anthropic API
    anthropic_api_key: str

    # Database
    database_url: str

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    allowed_origins: str = "http://localhost:3000"

    # ChromaDB
    chroma_persist_directory: str = "./chroma_db"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"

    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

settings = Settings()
