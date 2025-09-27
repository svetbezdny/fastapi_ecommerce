from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, update

from app.schemas import ProductCreate, Product as ProductSchema
from app.models import Product as ProductModel, Category as CategoryModel
from app.db_depends import get_db_dep


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: get_db_dep):
    return db.scalars(select(ProductModel).where(ProductModel.is_active)).all()


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(db: get_db_dep, product: ProductCreate):
    stmt = select(CategoryModel).where(
        CategoryModel.id == product.category_id, CategoryModel.is_active
    )
    category = db.scalars(stmt).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )
    new_product = ProductModel(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(db: get_db_dep, category_id: int):
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == category_id, CategoryModel.is_active
    )
    category = db.scalars(category_stmt).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    product_stmt = select(ProductModel).where(
        ProductModel.category_id == category_id, ProductModel.is_active
    )
    return db.scalars(product_stmt).all()


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(db: get_db_dep, product_id: int):
    product_stmt = select(ProductModel).where(
        ProductModel.id == product_id, ProductModel.is_active
    )
    product = db.scalars(product_stmt).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == product.category_id, CategoryModel.is_active
    )
    category = db.scalars(category_stmt).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )
    return product


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(db: get_db_dep, product_id: int, product: ProductCreate):
    stmt = select(ProductModel).where(
        ProductModel.id == product_id, ProductModel.is_active
    )
    exist_product = db.scalars(stmt).first()
    if not exist_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    category_stmt = select(CategoryModel).where(
        CategoryModel.id == product.category_id, CategoryModel.is_active
    )
    category = db.scalars(category_stmt).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(**product.model_dump())
    )
    db.commit()
    db.refresh(exist_product)
    return exist_product


@router.delete("/{product_id}")
async def delete_product(db: get_db_dep, product_id: int):
    product_stmt = select(ProductModel).where(
        ProductModel.id == product_id, ProductModel.is_active
    )
    product = db.scalars(product_stmt).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    category_stmt = select(CategoryModel).where(CategoryModel.id == product.category_id)
    category = db.scalars(category_stmt).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category not found"
        )
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(is_active=False)
    )
    db.commit()
    return {"status": "success", "message": "Product marked as inactive"}
