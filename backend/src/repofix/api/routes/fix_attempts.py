from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from repofix.db.session import get_db
from repofix.models import FixAttempt
from repofix.schemas import FixAttemptCreate, FixAttemptResponse


router = APIRouter(
    prefix="/api/fix-attempts",
    tags=["Fix Attempts"],
)


@router.post(
    "/",
    response_model=FixAttemptResponse,
)
def create_fix_attempt(
    attempt_data: FixAttemptCreate,
    db: Session = Depends(get_db),
):
    attempt = FixAttempt(
        issue_id=attempt_data.issue_id,
        attempt_number=attempt_data.attempt_number,
        status=attempt_data.status,
        patch=attempt_data.patch,
        test_output=attempt_data.test_output,
        error_message=attempt_data.error_message,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt