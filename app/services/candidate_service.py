from app.models.candidate import CandidateCreate, CandidateUpdate, CandidateInDB
from app.repositories.candidate_repository import CandidateRepository
from typing import List


class CandidateService:
    def __init__(self, repository: CandidateRepository):
        self.repository = repository

    async def create_candidate(self, candidate: CandidateCreate) -> CandidateInDB:
        return await self.repository.create(candidate)

    async def get_candidate(self, candidate_id: str) -> CandidateInDB | None:
        return await self.repository.get(candidate_id)

    async def update_candidate(
        self, candidate_id: str, candidate: CandidateUpdate
    ) -> CandidateInDB | None:
        return await self.repository.update(candidate_id, candidate)

    async def delete_candidate(self, candidate_id: str) -> bool:
        return await self.repository.delete(candidate_id)

    async def get_all_candidates(
        self, search_query: str | None = None
    ) -> List[CandidateInDB]:
        return await self.repository.get_all(search_query)

    async def generate_report(self) -> str:
        return await self.repository.generate_report()
