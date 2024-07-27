from uuid import UUID
from bson import UuidRepresentation
from motor.motor_asyncio import AsyncIOMotorClient
from models.candidate import CandidateCreate, CandidateUpdate, CandidateInDB
from core.config import settings
from typing import List
import csv
import io


class CandidateRepository:
    def __init__(self):
        self.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            uuidRepresentation=settings.UUID_REPRESENTATION,
        )
        self.database = self.client[settings.MONGODB_DB_NAME]
        self.collection = self.database["candidates"]

    async def create(self, candidate: CandidateCreate) -> CandidateInDB:
        candidate_in_db = CandidateInDB(**candidate.model_dump())
        await self.collection.insert_one(candidate_in_db.model_dump())
        return candidate_in_db

    async def get(self, candidate_id: str) -> CandidateInDB | None:
        candidate = await self.collection.find_one({"id": UUID(candidate_id)})
        if candidate:
            return CandidateInDB(**candidate)
        return None

    async def update(
        self, candidate_id: str, candidate: CandidateUpdate
    ) -> CandidateInDB | None:
        await self.collection.update_one(
            {"id": UUID(candidate_id)}, {"$set": candidate.model_dump()}
        )
        candidate_in_db = await self.get(candidate_id)
        if candidate_in_db:
            return candidate_in_db
        return None

    async def delete(self, candidate_id: str) -> bool:
        result = await self.collection.delete_one({"id": UUID(candidate_id)})
        return result.deleted_count > 0

    async def get_all(self, search_query: dict | None = None) -> List[CandidateInDB]:

        if search_query:
            query = search_query
            print("query:", query)
        else:
            query = {}
        cursor = self.collection.find(query)
        candidates = await cursor.to_list(length=None)
        return [CandidateInDB(**candidate) for candidate in candidates]

    async def generate_report(self) -> str:
        candidates = await self.get_all()
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=CandidateInDB.model_fields.keys())
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(candidate.model_dump())
        return output.getvalue()
