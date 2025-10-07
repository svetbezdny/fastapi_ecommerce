__all__ = ["routers"]


from .categories import router as categories_router
from .products import router as products_router
from .reviews import router as reviews_router
from .users import router as users_router

routers = [
    users_router,
    categories_router,
    products_router,
    reviews_router,
]
