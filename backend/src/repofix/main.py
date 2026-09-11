from fastapi import FastAPI

app = FastAPI(
    title="RepoFix AI",
    description="Autonomous GitHub Issue Resolution and Code Validation",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "application": "RepoFix AI",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }