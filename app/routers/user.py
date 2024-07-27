from fastapi import APIRouter, Depends, HTTPException
from app.models.user import UserCreate, UserInDB
from app.services.user_service import UserService
from app.core.security import get_current_user

router = APIRouter()


@router.post("/", response_model=UserInDB)
async def create_user(user: UserCreate, service: UserService = Depends()):
    return await service.create_user(user)
