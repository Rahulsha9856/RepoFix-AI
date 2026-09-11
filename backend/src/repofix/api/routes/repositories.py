from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from repofix.db.session import get_db
from repofix.models import Repository
from repofix.schemas import RepositoryCreate, RepositoryResponse
from repofix.github.client import GitHubClient


router = APIRouter(
    prefix="/api/repositories",
    tags=["Repositories"],
)


@router.post(
    "/",
    response_model=RepositoryResponse,
)
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

@router.get("/{full_name:path}")
def get_github_repository(full_name: str):
    client = GitHubClient()
    repository = client.get_repository(full_name)

    return {
        "github_repo_id": repository.id,
        "name": repository.name,
        "full_name": repository.full_name,
        "clone_url": repository.clone_url,
        "description": repository.description,
    }