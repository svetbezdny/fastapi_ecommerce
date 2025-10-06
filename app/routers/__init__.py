__all__ = ["routers"]


from .categories import router as categories_router
from .products import router as products_router
from .users import router as user_router

routers = [
    user_router,
    categories_router,
    products_router,
]
