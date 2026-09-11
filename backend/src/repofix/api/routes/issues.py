from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from repofix.db.session import get_db
from repofix.schemas import IssueCreate, IssueResponse
from repofix.github.client import GitHubClient
from repofix.models import Issue, Repository


router = APIRouter(
    prefix="/api/issues",
    tags=["Issues"],
)


@router.post(
    "/",
    response_model=IssueResponse,
)
def create_issue(
    issue_data: IssueCreate,
    db: Session = Depends(get_db),
):
    issue = Issue(
        github_issue_id=issue_data.github_issue_id,
        repository_id=issue_data.repository_id,
        number=issue_data.number,
        title=issue_data.title,
        description=issue_data.description,
        status=issue_data.status,
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue

@router.get("/{full_name:path}/{issue_number}")
def get_github_issue(
    full_name: str,
    issue_number: int,
):
    client = GitHubClient()
    issue = client.get_issue(full_name, issue_number)

    return {
        "github_issue_id": issue.id,
        "number": issue.number,
        "title": issue.title,
        "description": issue.body,
        "status": issue.state,
        "repository": issue.repository.full_name,
    }

@router.post("/sync/{full_name:path}/{issue_number}")
def sync_github_issue(
    full_name: str,
    issue_number: int,
    db: Session = Depends(get_db),
):
    client = GitHubClient()

    github_issue = client.get_issue(
        full_name,
        issue_number,
    )

    repository = db.query(Repository).filter(
        Repository.full_name == full_name
    ).first()

    if repository is None:
        raise ValueError(
            f"Repository '{full_name}' is not registered"
        )

    existing_issue = db.query(Issue).filter(
        Issue.github_issue_id == github_issue.id
    ).first()

    if existing_issue:
        return existing_issue

    issue = Issue(
        github_issue_id=github_issue.id,
        repository_id=repository.id,
        number=github_issue.number,
        title=github_issue.title,
        description=github_issue.body,
        status=github_issue.state,
    )

    db.add(issue)
    db.commit()
    db.refresh(issue)

    return issue

@router.get(
    "/",
    response_model=list[IssueResponse],
)
def get_issues(
    db: Session = Depends(get_db),
):
    return db.query(Issue).all()