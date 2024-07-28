import re
from app.models.candidate import CandidateCreate, CandidateUpdate, CandidateInDB
from app.repositories.candidate_repository import CandidateRepository
from typing import Dict, List


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

    def build_query(self, search_query: str) -> Dict:
        # This function parses the search query to build the appropriate MongoDB query
        # Here we assume the search query is in the format 'field:value'
        match = re.match(r"(\w+):(.+)", search_query)
        if match:
            field, value = match.groups()
            return {field: value}
        else:
            return {"$text": {"$search": search_query}}

    async def get_all_candidates(
        self, search_query: str | None = None
    ) -> List[CandidateInDB]:
        if search_query:
            query = self.build_query(search_query)
            return await self.repository.get_all(query)
        return await self.repository.get_all()

    async def generate_report(self) -> str:
        return await self.repository.generate_report()
