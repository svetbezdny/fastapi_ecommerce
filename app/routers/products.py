from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update

from app.auth import get_current_seller
from app.db_depends import get_db_dep
from app.models import Category as CategoryModel
from app.models import Product as ProductModel
from app.models import User as UserModel
from app.schemas import Product as ProductSchema
from app.schemas import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: get_db_dep):
    result = await db.scalars(select(ProductModel).where(ProductModel.is_active))
    return result.all()


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    db: get_db_dep, product: ProductCreate, current_user: Annotated[UserModel, Depends(get_current_seller)]
):
    stmt = select(CategoryModel).where(CategoryModel.id == product.category_id, CategoryModel.is_active)
    category = await db.scalars(stmt)
    category_result = category.first()
    if not category_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")
    new_product = ProductModel(**product.model_dump(), seller_id=current_user.id)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(db: get_db_dep, category_id: int):
    category_stmt = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active)
    category = await db.scalars(category_stmt)
    result_category = category.first()
    if not result_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    product_stmt = select(ProductModel).where(ProductModel.category_id == category_id, ProductModel.is_active)
    result = await db.scalars(product_stmt)
    return result.all()


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(db: get_db_dep, product_id: int):
    product_stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active)
    product = await db.scalars(product_stmt)
    product_result = product.first()
    if not product_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    category_stmt = select(CategoryModel).where(CategoryModel.id == product_result.category_id, CategoryModel.is_active)
    category = await db.scalars(category_stmt)
    category_result = category.first()
    if not category_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")
    return product_result


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    db: get_db_dep,
    product_id: int,
    product: ProductCreate,
    current_user: Annotated[UserModel, Depends(get_current_seller)],
):
    stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active)
    exist_product = await db.scalars(stmt)
    product_result = exist_product.first()
    if not product_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product_result.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")
    category_stmt = select(CategoryModel).where(CategoryModel.id == product.category_id, CategoryModel.is_active)
    category = await db.scalars(category_stmt)
    category_result = category.first()
    if not category_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")
    await db.execute(
        update(ProductModel).where(ProductModel.id == product_id).values(**product.model_dump(exclude_unset=True))
    )
    await db.commit()
    await db.refresh(product_result)
    return product_result


@router.delete("/{product_id}", response_model=ProductSchema)
async def delete_product(
    db: get_db_dep,
    product_id: int,
    current_user: Annotated[UserModel, Depends(get_current_seller)],
):
    product_stmt = select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active)
    product = await db.scalars(product_stmt)
    product_result = product.first()
    if not product_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product_result.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own products")
    category_stmt = select(CategoryModel).where(CategoryModel.id == product_result.category_id)
    category = await db.scalars(category_stmt)
    category_result = category.first()
    if not category_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found")
    await db.execute(update(ProductModel).where(ProductModel.id == product_id).values(is_active=False))
    await db.commit()
    await db.refresh(product_result)
    return product_result
