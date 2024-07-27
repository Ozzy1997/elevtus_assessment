from pydantic_settings import BaseSettings
from pydantic import Field
from bson import UuidRepresentation
from pydantic.json import pydantic_encoder
from typing import Any


class Settings(BaseSettings):
    PROJECT_NAME: str = "Candidate Profile Management"
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "candidate_profile_db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UUID_REPRESENTATION: str = "standard"


settings = Settings()
