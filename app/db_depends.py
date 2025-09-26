from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Generator
from typing import Annotated

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db_dep = Annotated[Session, Depends(get_db)]
