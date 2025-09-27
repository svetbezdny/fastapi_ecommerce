from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveFloat, PositiveInt


class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Название категории (3-50 символов)")
    parent_id: int | None = Field(default=None, description="ID родительской категории, если есть")


class Category(CategoryCreate):
    id: PositiveInt = Field(description="Уникальный идентификатор категории")
    is_active: bool = Field(description="Активность категории")

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100, description="Название товара (3-100 символов)")
    description: str | None = Field(default=None, max_length=500, description="Описание товара (до 500 символов)")
    price: PositiveFloat = Field(description="Цена товара (больше 0)")
    image_url: str | None = Field(default=None, max_length=200, description="URL изображения товара")
    stock: NonNegativeInt = Field(description="Количество товара на складе (0 или больше)")
    category_id: int = Field(description="ID категории, к которой относится товар")


class Product(ProductCreate):
    id: PositiveInt = Field(description="Уникальный идентификатор товара")
    is_active: bool = Field(description="Активность товара")

    model_config = ConfigDict(from_attributes=True)
