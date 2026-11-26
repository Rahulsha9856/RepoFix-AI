from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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