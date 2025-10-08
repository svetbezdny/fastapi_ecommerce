from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session


get_db_dep = Annotated[AsyncSession, Depends(get_db)]
