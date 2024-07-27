from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from services.user_service import UserService
from repositories.user_repository import UserRepository
from repositories.candidate_repository import CandidateRepository
from services.candidate_service import CandidateService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_repository():
    return UserRepository()


def get_candidate_repository():
    return CandidateRepository()


def get_user_service():
    return UserService(get_user_repository())


def get_candidate_service():
    return CandidateService(get_candidate_repository())


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
):
    email = decode_access_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
