from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import UserCreate, UserInDB
from app.core.config import settings
from bson import UuidRepresentation
from uuid import UUID


class UserRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            uuidRepresentation=settings.UUID_REPRESENTATION,
        )
        self.database = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.database["users"]

    async def create(self, user: UserInDB) -> UserInDB:
        user_dict = user.model_dump()
        await self.collection.insert_one(user_dict)
        return user

    async def get_by_email(self, email: str) -> UserInDB | None:
        user = await self.collection.find_one({"email": email})
        if user:
            return UserInDB(**user)
        return None

    async def update(self, email: str, update_data: dict) -> UserInDB | None:
        await self.collection.update_one({"email": email}, {"$set": update_data})
        return await self.get_by_email(email)
