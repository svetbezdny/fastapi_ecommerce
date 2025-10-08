from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.auth import get_current_role
from app.db_utils import get_db_dep, update_product_rating
from app.models import Product as ProductModel
from app.models import Review as ReviewModel
from app.models import User as UserModel
from app.schemas import Review as ReviewSchema
from app.schemas import ReviewCreate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: get_db_dep):
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active))
    return result.all()


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
    db: get_db_dep,
    review: ReviewCreate,
    current_user: Annotated[UserModel, Depends(get_current_role("buyer"))],
):
    result = await db.execute(select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    new_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    await update_product_rating(db, product.id)
    return new_review


@router.get("/products/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_product_reviews(db: get_db_dep, product_id: int):
    product_result = await db.scalars(select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active))
    product = product_result.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    reviews_result = await db.scalars(
        select(ReviewModel).where(ReviewModel.product_id == product.id, ProductModel.is_active)
    )
    return reviews_result.all()


@router.delete("/reviews/{review_id}")
async def delete_review(
    db: get_db_dep,
    review_id: int,
    _: Annotated[UserModel, Depends(get_current_role("admin"))],
):
    result = await db.execute(select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )
    review.is_active = False
    await db.commit()
    await update_product_rating(db, review.product_id)
    return {"message": "Review deleted"}
