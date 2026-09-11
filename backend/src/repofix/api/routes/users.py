from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from repofix.db.session import get_db
from repofix.models import User
from repofix.schemas import UserCreate, UserResponse


router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    user = User(
        github_id=user_data.github_id,
        username=user_data.username,
        email=user_data.email,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return db.query(User).all()