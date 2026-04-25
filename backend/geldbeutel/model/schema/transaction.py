from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic_core.core_schema import ValidationInfo

from model.domain.transaction import TransactionType


class AddTransactionModel(BaseModel):
    """
    Model for add transaction request
    """
    title: str
    type: TransactionType
    amount: float
    date: datetime
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Transaction name cannot be empty")
        return v.strip()

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Transaction amount must be positive")
        return v

class UpdateTransactionRequest(BaseModel):
    """
    Model for update transaction request
    """
    title: str
    type: TransactionType
    amount: float
    date: datetime
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Transaction name cannot be empty")
        return v.strip()

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Transaction amount must be positive")
        return v


class PatchTransactionRequest(BaseModel):
    """
    Model for patch transaction request
    """
    title: Optional[str] = None
    type: Optional[TransactionType] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Transaction name cannot be empty")
        return v.strip()

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Transaction amount must be positive")
        return v

class ListTransactionResponse(BaseModel):
    """
    Model for list transaction response
    """
    id: int
    title: str
    type: TransactionType
    amount: float
    date: datetime
    category_id: Optional[int] = None

    # Needed for populating the model from ORM result
    model_config = ConfigDict(from_attributes=True)
