from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    github_id: str
    username: str
    email: str | None = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)