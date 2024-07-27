from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import UserCreate, UserInDB
from app.core.config import settings


class UserRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.database = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.database["users"]

    async def create(self, user: UserCreate) -> UserInDB:
        user_in_db = UserInDB(**user.model_dump())
        await self.collection.insert_one(user_in_db.model_dump())
        return user_in_db

    async def get_by_email(self, email: str) -> UserInDB | None:
        user = await self.collection.find_one({"email": email})
        if user:
            return UserInDB(**user)
        return None
