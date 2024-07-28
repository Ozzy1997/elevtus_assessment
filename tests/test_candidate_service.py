# tests/test_candidate_service.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.candidate_service import CandidateService
from app.models.candidate import CandidateCreate, CandidateUpdate, CandidateInDB
from uuid import UUID
from typing import List


@pytest.fixture
def candidate_repository_mock():
    return AsyncMock()


@pytest.fixture
def candidate_service(candidate_repository_mock):
    return CandidateService(candidate_repository_mock)


@pytest.fixture
def sample_candidate_data():
    return {
        "id": UUID("12345678-1234-5678-1234-567812345678"),
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "career_level": "Senior",
        "job_major": "Computer Science",
        "years_of_experience": 5,
        "degree_type": "Master",
        "skills": ["Python", "FastAPI"],
        "nationality": "US",
        "city": "New York",
        "salary": 100000,
        "gender": "Female",
    }


@pytest.mark.asyncio
async def test_create_candidate(
    candidate_service, candidate_repository_mock, sample_candidate_data
):
    # Arrange
    candidate_create = CandidateCreate(
        **{k: v for k, v in sample_candidate_data.items() if k != "id"}
    )
    candidate_repository_mock.create.return_value = CandidateInDB(
        **sample_candidate_data
    )

    # Act
    result = await candidate_service.create_candidate(candidate_create)

    # Assert
    assert result.dict() == sample_candidate_data
    candidate_repository_mock.create.assert_called_once_with(candidate_create)


@pytest.mark.asyncio
async def test_get_candidate(
    candidate_service, candidate_repository_mock, sample_candidate_data
):
    # Arrange
    candidate_id = str(sample_candidate_data["id"])
    candidate_repository_mock.get.return_value = CandidateInDB(**sample_candidate_data)

    # Act
    result = await candidate_service.get_candidate(candidate_id)

    # Assert
    assert result.dict() == sample_candidate_data
    candidate_repository_mock.get.assert_called_once_with(candidate_id)


@pytest.mark.asyncio
async def test_get_candidate_not_found(candidate_service, candidate_repository_mock):
    # Arrange
    candidate_id = "nonexistent-id"
    candidate_repository_mock.get.return_value = None

    # Act
    result = await candidate_service.get_candidate(candidate_id)

    # Assert
    assert result is None
    candidate_repository_mock.get.assert_called_once_with(candidate_id)


@pytest.mark.asyncio
async def test_update_candidate(
    candidate_service, candidate_repository_mock, sample_candidate_data
):
    # Arrange
    candidate_id = str(sample_candidate_data["id"])
    update_data = CandidateUpdate(
        first_name="John",
        last_name="Smith",
        email="email@email.com",
        career_level="Junior",
        job_major="Data Science",
        years_of_experience=3,
        degree_type="Bachelor",
        skills=["Python", "SQL"],
        city="San Francisco",
        gender="Male",
        nationality="UK",
        salary=80000,
    )
    updated_candidate = {
        **sample_candidate_data,
        **update_data.model_dump(exclude_unset=True),
    }
    candidate_repository_mock.update.return_value = CandidateInDB(**updated_candidate)

    # Act
    result = await candidate_service.update_candidate(candidate_id, update_data)

    # Assert
    assert result.dict() == updated_candidate
    candidate_repository_mock.update.assert_called_once_with(candidate_id, update_data)


@pytest.mark.asyncio
async def test_delete_candidate(candidate_service, candidate_repository_mock):
    # Arrange
    candidate_id = "12345678-1234-5678-1234-567812345678"
    candidate_repository_mock.delete.return_value = True

    # Act
    result = await candidate_service.delete_candidate(candidate_id)

    # Assert
    assert result is True
    candidate_repository_mock.delete.assert_called_once_with(candidate_id)


@pytest.mark.asyncio
async def test_get_all_candidates(
    candidate_service, candidate_repository_mock, sample_candidate_data
):
    # Arrange
    candidates = [CandidateInDB(**sample_candidate_data) for _ in range(3)]
    candidate_repository_mock.get_all.return_value = candidates

    # Act
    result = await candidate_service.get_all_candidates()

    # Assert
    assert len(result) == 3
    assert all(isinstance(candidate, CandidateInDB) for candidate in result)
    candidate_repository_mock.get_all.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_all_candidates_with_search(
    candidate_service, candidate_repository_mock, sample_candidate_data
):
    # Arrange
    search_query = "Python"
    candidates = [CandidateInDB(**sample_candidate_data) for _ in range(2)]
    candidate_repository_mock.get_all.return_value = candidates

    # Act
    result = await candidate_service.get_all_candidates(search_query)

    # Assert
    assert len(result) == 2
    assert all(isinstance(candidate, CandidateInDB) for candidate in result)
    candidate_repository_mock.get_all.assert_called_once_with(
        {"$text": {"$search": search_query}}
    )


@pytest.mark.asyncio
async def test_generate_report(candidate_service, candidate_repository_mock):
    # Arrange
    report_content = "CSV report content"
    candidate_repository_mock.generate_report.return_value = report_content

    # Act
    result = await candidate_service.generate_report()

    # Assert
    assert result == report_content
    candidate_repository_mock.generate_report.assert_called_once()


def test_build_query(candidate_service):
    # Test with field:value format
    assert candidate_service.build_query("career_level:Senior") == {
        "career_level": "Senior"
    }

    # Test with simple search term
    assert candidate_service.build_query("Python") == {"$text": {"$search": "Python"}}

    # Test with complex search term
    assert candidate_service.build_query("Software Engineer") == {
        "$text": {"$search": "Software Engineer"}
    }
