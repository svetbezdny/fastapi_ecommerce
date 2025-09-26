from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ECHO,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)
