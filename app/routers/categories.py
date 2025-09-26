from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, update


from app.models import Category as CategoryModel
from app.schemas import CategoryCreate, Category as CategorySchema
from app.db_depends import get_db_dep

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db: get_db_dep):
    stmt = select(CategoryModel).where(CategoryModel.is_active)
    return db.scalars(stmt).all()


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(db: get_db_dep, category: CategoryCreate):
    if category.parent_id:
        stmt = select(CategoryModel).where(
            CategoryModel.id == category.parent_id, CategoryModel.is_active
        )
        parent = db.scalars(stmt).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )
    new_category = CategoryModel(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(db: get_db_dep, category_id: int, category: CategoryCreate):
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.is_active
    )
    exist_category = db.scalars(stmt).first()
    if not exist_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found",
        )
    if exist_category.parent_id:
        parent_stmt = select(CategoryModel).where(
            CategoryModel.id == exist_category.parent_id, CategoryModel.is_active
        )
        parent = db.scalars(parent_stmt).first()
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parent category not found",
            )
    db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(**category.model_dump())
    )
    db.commit()
    db.refresh(exist_category)
    return exist_category


@router.delete("/{category_id}")
async def delete_category(db: get_db_dep, category_id: int):
    stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.is_active
    )
    category = db.scalars(stmt).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found",
        )
    db.execute(
        update(CategoryModel)
        .where(CategoryModel.id == category_id)
        .values(is_active=False)
    )
    db.commit()
    return {"status": "success", "message": "Category marked as inactive"}
