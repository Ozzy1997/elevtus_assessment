from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: UUID = Field(default_factory=uuid4)
    hashed_password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserOut(UserBase):
    id: UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
