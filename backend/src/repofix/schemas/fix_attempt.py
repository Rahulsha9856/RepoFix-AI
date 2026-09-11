from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FixAttemptBase(BaseModel):
    issue_id: int
    attempt_number: int
    status: str = "started"
    patch: str | None = None
    test_output: str | None = None
    error_message: str | None = None


class FixAttemptCreate(FixAttemptBase):
    pass


class FixAttemptResponse(FixAttemptBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)