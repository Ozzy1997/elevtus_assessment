from fastapi import FastAPI
from app.core.config import settings
from app.routers import user, candidate
from app.routers import auth
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager


async def create_indexes():
    client = AsyncIOMotorClient(
        settings.MONGODB_URL, uuidRepresentation=settings.UUID_REPRESENTATION
    )
    db = client[settings.MONGODB_DB_NAME]
    await db["candidates"].create_index(
        [
            ("first_name", "text"),
            ("last_name", "text"),
            ("email", "text"),
            ("career_level", "text"),
            ("job_major", "text"),
            ("degree_type", "text"),
            ("skills", "text"),
            ("nationality", "text"),
            ("city", "text"),
        ]
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


@app.get("/health", status_code=200)
async def health_check():
    return {"status": "OK"}


app.include_router(auth.router, tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(candidate.router, prefix="/candidate", tags=["candidate"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
