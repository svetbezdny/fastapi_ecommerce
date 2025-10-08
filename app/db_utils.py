from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.sql import func

from app.db_depends import get_db_dep
from app.models import Product as ProductModel
from app.models import Review as ReviewModel


async def update_product_rating(db: get_db_dep, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(ReviewModel.product_id == product_id, ReviewModel.is_active)
    )
    avg_rating = result.scalar()
    avg_rating = 0.0 if avg_rating is None else round(avg_rating, 2)
    product = await db.get(ProductModel, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    if product.rating != avg_rating:
        product.rating = avg_rating
        await db.commit()
        await db.refresh(product)
