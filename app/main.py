from fastapi import FastAPI
from app.core.config import settings
from app.routers import user, candidate

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health", status_code=200)
async def health_check():
    return {"status": "OK"}


app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(candidate.router, prefix="/candidate", tags=["candidate"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
