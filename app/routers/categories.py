from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, update

from app.db_depends import get_db_dep
from app.models import Category as CategoryModel
from app.schemas import Category as CategorySchema
from app.schemas import CategoryCreate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: get_db_dep):
    stmt = select(CategoryModel).where(CategoryModel.is_active)
    result = await db.scalars(stmt)
    return result.all()


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(db: get_db_dep, category: CategoryCreate):
    if category.parent_id:
        stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id, CategoryModel.is_active)
        result = await db.scalars(stmt)
        parent = result.first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )
    new_category = CategoryModel(**category.model_dump())
    db.add(new_category)
    await db.commit()
    return new_category


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(db: get_db_dep, category_id: int, category: CategoryCreate):
    stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active)
    exist_category = await db.scalars(stmt)
    result_category = exist_category.first()
    if not result_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found",
        )
    if result_category.parent_id:
        parent_stmt = select(CategoryModel).where(
            CategoryModel.id == result_category.parent_id, CategoryModel.is_active
        )
        parent = await db.scalars(parent_stmt)
        parent_result = parent.first()
        if not parent_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )
    await db.execute(
        update(CategoryModel).where(CategoryModel.id == category_id).values(**category.model_dump(exclude_unset=True))
    )
    await db.commit()
    return result_category


@router.delete("/{category_id}", response_model=CategorySchema)
async def delete_category(db: get_db_dep, category_id: int):
    stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active)
    category = await db.scalars(stmt)
    result = category.first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found",
        )
    await db.execute(update(CategoryModel).where(CategoryModel.id == category_id).values(is_active=False))
    await db.commit()
    return result
