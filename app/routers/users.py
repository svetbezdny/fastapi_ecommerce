from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.auth import hash_password
from app.db_depends import get_db_dep
from app.models import User as UserModel
from app.schemas import User as UserSchema
from app.schemas import UserCreate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(db: get_db_dep, user: UserCreate):
    email_check = await db.scalars(select(UserModel).where(UserModel.email == user.email))
    if email_check.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    new_user = UserModel(email=user.email, hashed_password=hash_password(user.password), role=user.role)
    db.add(new_user)
    await db.commit()
    return new_user
