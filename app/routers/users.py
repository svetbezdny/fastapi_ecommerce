from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from app.auth import create_access_token, create_refresh_token, hash_password, verify_password
from app.config import settings
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


@router.post("/token")
async def login_user(db: get_db_dep, form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    result = await db.scalars(select(UserModel).where(UserModel.email == form.username))
    user = result.first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
    refresh_token = create_refresh_token(data={"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh-token")
async def refresh_token(db: get_db_dep, refresh_token: str):
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise exc
    except jwt.PyJWTError:
        raise exc from None
    result = await db.scalars(select(UserModel).where(UserModel.email == email, UserModel.is_active))
    user = result.first()
    if not user:
        raise exc
    access_token = create_access_token(data={"sub": user.email, "role": user.role, "id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
