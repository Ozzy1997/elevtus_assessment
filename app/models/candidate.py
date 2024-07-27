from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from typing import List, Literal


class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: float
    gender: Literal["Male", "Female"]


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(CandidateBase):
    pass


class CandidateInDB(CandidateBase):
    id: UUID = Field(default_factory=uuid4)
