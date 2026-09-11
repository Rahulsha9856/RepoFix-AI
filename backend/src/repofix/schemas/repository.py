from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RepositoryBase(BaseModel):
    github_repo_id: int
    name: str
    full_name: str
    clone_url: str
    owner_id: int


class RepositoryCreate(RepositoryBase):
    pass


class RepositoryResponse(RepositoryBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)