__all__ = ["routers"]


from .categories import router as categories_router
from .products import router as products_router


routers = [
    categories_router,
    products_router,
]
