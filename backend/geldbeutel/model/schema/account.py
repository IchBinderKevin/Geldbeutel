from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class AddAccountRequest(BaseModel):
    """
    Model for add account request
    """
    name: str
    balance: float

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Account name cannot be empty")
        return v.strip()


class UpdateAccountRequest(BaseModel):
    """
    Model for update account request
    """
    name: str
    balance: float

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("New account name cannot be empty")
        return v.strip()


class PatchAccountRequest(BaseModel):
    """
    Model for patch account request
    """
    name: Optional[str] = None
    balance: Optional[float] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if v.strip() == "":
                raise ValueError("New account name cannot be empty")
            return v.strip()
        return v

class ListAccountResponse(BaseModel):
    """
    Model for list account response
    """
    id: int
    name: str
    balance: float
    created_at: datetime
    updated_at: datetime

    # Needed for populating the model from ORM result
    model_config = ConfigDict(from_attributes=True)
