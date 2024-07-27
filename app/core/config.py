from pydantic_settings import BaseSettings
from pydantic import Field
from bson import UuidRepresentation
from pydantic.json import pydantic_encoder
from typing import Any
import os

import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Candidate Profile API")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "candidate_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    UUID_REPRESENTATION: str = "standard"


settings = Settings()
