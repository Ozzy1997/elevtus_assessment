from fastapi import APIRouter, Depends, HTTPException
from models.user import UserCreate, UserInDB
from services.user_service import UserService
from core.deps import get_user_service

router = APIRouter()


@router.post("/", response_model=UserInDB)
async def create_user(
    user: UserCreate, service: UserService = Depends(get_user_service)
):
    try:
        return await service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{email}", response_model=UserInDB)
async def get_user_by_email(
    email: str, service: UserService = Depends(get_user_service)
):
    try:
        return await service.get_user_by_email(email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
