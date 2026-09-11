from fastapi import FastAPI

from repofix.api.routes.health import router as health_router
from repofix.api.routes.users import router as users_router
from repofix.api.routes.repositories import router as repositories_router
from repofix.api.routes.issues import router as issues_router
from repofix.api.routes.fix_attempts import router as fix_attempts_router

app = FastAPI(
    title="RepoFix AI",
    description="Autonomous GitHub Issue Resolution and Code Validation",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(repositories_router)
app.include_router(issues_router)
app.include_router(fix_attempts_router)


@app.get("/")
async def root():
    return {
        "application": "RepoFix AI",
        "status": "running",
        "version": "0.1.0",
    }