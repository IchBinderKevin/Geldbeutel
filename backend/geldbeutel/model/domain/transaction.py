from datetime import datetime, UTC
from enum import Enum

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.domain import BaseDomainModel

class TransactionType(Enum):
    EXPENSE = "expense"
    INCOME = "income"

class Transaction(BaseDomainModel):
    """
    ORM Model for transaction table
    """
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[TransactionType] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)

    category = relationship("Category")
