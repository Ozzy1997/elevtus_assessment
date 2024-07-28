from app.models.user import UserCreate, UserInDB
from app.repositories.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password
from uuid import uuid4


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user: UserCreate) -> UserInDB:
        if await self.repository.get_by_email(user.email):
            raise Exception("User with this email already exists")

        hashed_password = get_password_hash(user.password)
        user_in_db = UserInDB(
            id=uuid4(),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
        )

        return await self.repository.create(user_in_db)

    async def authenticate_user(self, email: str, password: str) -> UserInDB | None:
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_user_by_email(self, email: str) -> UserInDB | None:

        return await self.repository.get_by_email(email)
