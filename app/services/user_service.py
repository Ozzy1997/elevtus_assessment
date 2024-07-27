from app.models.user import UserCreate, UserInDB
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserCreate) -> UserInDB:
        return await self.repository.create(user)

    async def get_user_by_email(self, email: str) -> UserInDB | None:
        return await self.repository.get_by_email(email)
