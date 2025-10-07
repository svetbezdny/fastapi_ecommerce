from datetime import datetime

from sqlalchemy import CheckConstraint, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Review(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    grade: Mapped[int] = mapped_column(
        CheckConstraint("grade >= 1 and grade <= 5"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(default=True)
