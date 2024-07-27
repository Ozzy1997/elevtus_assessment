from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserInDB(UserBase):
    id: UUID = Field(default_factory=uuid4)
