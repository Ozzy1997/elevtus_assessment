import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.user_service import UserService
from app.models.user import UserCreate, UserInDB
from uuid import UUID


@pytest.fixture
def user_repository_mock():
    return AsyncMock()


@pytest.fixture
def user_service(user_repository_mock):
    return UserService(user_repository_mock)


@pytest.mark.asyncio
async def test_create_user(user_service, user_repository_mock):
    # Arrange
    user_create = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="password123",
    )
    user_repository_mock.get_by_email.return_value = None
    user_repository_mock.create.return_value = UserInDB(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        hashed_password="hashed_password",
    )

    # Act
    result = await user_service.create_user(user_create)

    # Assert
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    assert result.email == "john@example.com"
    assert isinstance(result.id, UUID)
    user_repository_mock.get_by_email.assert_called_once_with("john@example.com")
    user_repository_mock.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_existing_email(user_service, user_repository_mock):
    # Arrange
    user_create = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="password123",
    )
    user_repository_mock.get_by_email.return_value = UserInDB(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        first_name="Existing",
        last_name="User",
        email="john@example.com",
        hashed_password="hashed_password",
    )

    # Act & Assert
    with pytest.raises(Exception, match="User with this email already exists"):
        await user_service.create_user(user_create)

    user_repository_mock.get_by_email.assert_called_once_with("john@example.com")
    user_repository_mock.create.assert_not_called()
