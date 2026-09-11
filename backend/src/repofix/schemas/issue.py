from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IssueBase(BaseModel):
    github_issue_id: int
    repository_id: int
    number: int
    title: str
    description: str | None = None
    status: str = "open"


class IssueCreate(IssueBase):
    pass


class IssueResponse(IssueBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)