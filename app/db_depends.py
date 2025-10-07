from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from app.database import async_session_maker
from app.models import Product as ProductModel
from app.models import Review as ReviewModel


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


get_db_dep = Annotated[AsyncSession, Depends(get_db)]


async def update_product_rating(db: get_db_dep, product_id: int) -> bool:
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(ReviewModel.product_id == product_id, ReviewModel.is_active)
    )
    avg_rating = result.scalar()
    avg_rating = 0.0 if avg_rating is None else round(avg_rating, 2)
    product = await db.get(ProductModel, product_id)
    if not product:
        return False
    if product.rating != avg_rating:
        product.rating = avg_rating
        await db.commit()
        await db.refresh(product)
    return True
