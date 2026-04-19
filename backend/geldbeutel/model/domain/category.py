from datetime import datetime, UTC

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, MappedColumn, mapped_column

from model.domain import BaseDomainModel


class Category(BaseDomainModel):
    """
    ORM Model for category table
    """
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    icon: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    color: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))
