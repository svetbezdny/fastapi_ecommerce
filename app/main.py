from fastapi import FastAPI
from fastapi.responses import RedirectResponse, ORJSONResponse

from app.routers import routers
from app.config import settings

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    default_response_class=ORJSONResponse,
)


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse("/docs")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL,
    )
