from fastapi import APIRouter, Depends, HTTPException
from app.models.candidate import CandidateCreate, CandidateUpdate, CandidateInDB
from app.models.user import UserInDB
from app.services.candidate_service import CandidateService
from app.core.security import get_current_user
from typing import List

router = APIRouter()


@router.post("/", response_model=CandidateInDB)
async def create_candidate(
    candidate: CandidateCreate,
    service: CandidateService = Depends(),
    current_user: UserInDB = Depends(get_current_user),
):
    return await service.create_candidate(candidate)


@router.get("/{candidate_id}", response_model=CandidateInDB)
async def get_candidate(
    candidate_id: str,
    service: CandidateService = Depends(),
    current_user: UserInDB = Depends(get_current_user),
):
    candidate = await service.get_candidate(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.put("/{candidate_id}", response_model=CandidateInDB)
async def update_candidate(
    candidate_id: str,
    candidate: CandidateUpdate,
    service: CandidateService = Depends(),
    current_user: UserInDB = Depends(get_current_user),
):
    updated_candidate = await service.update_candidate(candidate_id, candidate)
    if not updated_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return updated_candidate


@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: str,
    service: CandidateService = Depends(),
    current_user: UserInDB = Depends(get_current_user),
):
    deleted = await service.delete_candidate(candidate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully"}


@router.get("/all-candidates", response_model=List[CandidateInDB])
async def get_all_candidates(
    search_query: str | None = None,
    service: CandidateService = Depends(),
    current_user: UserInDB = Depends(get_current_user),
):
    if search_query:
        return await service.get_all_candidates(search_query)
    return await service.get_all_candidates()


@router.get("/generate-report")
async def generate_report(
    service: CandidateService = Depends(),
    current_user: UserInDB = Depends(get_current_user),
):
    report = await service.generate_report()
    return {"report": report}
