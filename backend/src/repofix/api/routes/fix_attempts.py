from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from repofix.db.session import get_db
from repofix.models import FixAttempt, Issue, Repository
from repofix.services.fix_workflow import FixWorkflow

router = APIRouter(
    prefix="/api/fix-attempts",
    tags=["Fix Attempts"],
)


@router.post("/run/{issue_id}")
def run_fix_workflow(
    issue_id: int,
    db: Session = Depends(get_db),
):
    issue = db.query(Issue).filter(
        Issue.id == issue_id
    ).first()

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    repository = db.query(Repository).filter(
        Repository.id == issue.repository_id
    ).first()

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    run_id = uuid4().hex[:8]

    branch_name = f"repofix/fix-issue-{issue.number}-{run_id}"

    workflow = FixWorkflow()

    result = workflow.run(
        repository=repository,
        issue=issue,
        workspace_path=(
            f"C:\\Users\\Rahul\\RepoFix-AI\\workspace\\"
            f"issue-{issue.id}-{run_id}"
        ),
        branch_name=branch_name,
    )

    return result

@router.get("/{issue_id}")
def get_fix_attempts(
    issue_id: int,
    db: Session = Depends(get_db),
):
    issue = db.query(Issue).filter(
        Issue.id == issue_id
    ).first()

    if issue is None:
        raise HTTPException(
            status_code=404,
            detail="Issue not found",
        )

    attempts = db.query(FixAttempt).filter(
        FixAttempt.issue_id == issue_id
    ).order_by(
        FixAttempt.attempt_number
    ).all()

    return attempts