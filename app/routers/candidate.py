import io
from fastapi import APIRouter, Depends, HTTPException
from app.models.candidate import CandidateCreate, CandidateUpdate, CandidateInDB
from app.services.candidate_service import CandidateService
from app.core.deps import get_candidate_service, get_current_user
from app.models.user import UserInDB
from typing import List
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.post("/", response_model=CandidateInDB)
async def create_candidate(
    candidate: CandidateCreate,
    service: CandidateService = Depends(get_candidate_service),
    current_user: UserInDB = Depends(get_current_user),
):
    return await service.create_candidate(candidate)


@router.get("/get_by_id", response_model=CandidateInDB)
async def get_candidate(
    candidate_id: str,
    service: CandidateService = Depends(get_candidate_service),
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
    service: CandidateService = Depends(get_candidate_service),
    current_user: UserInDB = Depends(get_current_user),
):
    updated_candidate = await service.update_candidate(candidate_id, candidate)
    if not updated_candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return updated_candidate


@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: str,
    service: CandidateService = Depends(get_candidate_service),
    current_user: UserInDB = Depends(get_current_user),
):
    deleted = await service.delete_candidate(candidate_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return {"message": "Candidate deleted successfully"}


@router.get(
    "/all-candidates",
    response_model=List[CandidateInDB],
    summary="Get all candidates",
    description=(
        "Fetch all candidates from the database. Optionally, you can provide a search query to filter results. "
        "The search query can be a simple text search or a specific field search in the format `field:value`.\n\n"
        "Examples:\n"
        "- `search_query=John` will search across all text-indexed fields for 'John'.\n"
        "- `search_query=email:john@example.com` will search for candidates with the email 'john@example.com'."
    ),
    response_description="A list of candidates matching the search criteria.",
)
async def get_all_candidates(
    search_query: str | None = None,
    service: CandidateService = Depends(get_candidate_service),
    current_user: UserInDB = Depends(get_current_user),
):
    if search_query:
        return await service.get_all_candidates(search_query)
    return await service.get_all_candidates()


@router.get("/generate-report")
async def generate_report(
    service: CandidateService = Depends(get_candidate_service),
    current_user: UserInDB = Depends(get_current_user),
):
    report = await service.generate_report()
    response = StreamingResponse(io.StringIO(report), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=report.csv"
    return response
