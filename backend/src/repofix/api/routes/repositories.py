
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from github import GithubException

from repofix.db.session import get_db
from repofix.models import Repository
from repofix.schemas import RepositoryCreate, RepositoryResponse
from repofix.github.client import GitHubClient


router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"],
)


# List repositories stored in PostgreSQL
@router.get("/", response_model=list[RepositoryResponse])
def list_repositories(db: Session = Depends(get_db)):
    return db.query(Repository).all()


# Create a repository
@router.post("/", response_model=RepositoryResponse)
def create_repository(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db),
):
    repository = Repository(
        github_repo_id=repository_data.github_repo_id,
        name=repository_data.name,
        full_name=repository_data.full_name,
        clone_url=repository_data.clone_url,
        owner_id=repository_data.owner_id,
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


# Fetch a repository from GitHub
@router.get("/{full_name:path}")
def get_github_repository(full_name: str):
    if not full_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Repository name is required. Use owner/repository.",
        )

    try:
        client = GitHubClient()
        repository = client.get_repository(full_name)

        return {
            "github_repo_id": repository.id,
            "name": repository.name,
            "full_name": repository.full_name,
            "clone_url": repository.clone_url,
            "description": repository.description,
        }

    except GithubException as error:
        raise HTTPException(
            status_code=error.status,
            detail="GitHub repository not found or access denied.",
        )
