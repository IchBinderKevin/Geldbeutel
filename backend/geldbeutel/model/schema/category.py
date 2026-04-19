from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class AddCategoryRequest(BaseModel):
    """
    Model for add category request
    """
    name: str
    icon: str
    description: str
    color: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("Account name cannot be empty")
        return v.strip()


class UpdateCategoryRequest(BaseModel):
    """
    Model for update category request
    """
    name: str
    icon: str
    description: str
    color: str
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("New account name cannot be empty")
        return v.strip()


class PatchCategoryRequest(BaseModel):
    """
    Model for patch category request
    """
    name: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if v.strip() == "":
                raise ValueError("New account name cannot be empty")
            return v.strip()
        return v

class ListCategoryResponse(BaseModel):
    """
    Model for list category response
    """
    id: int
    name: str
    icon: str
    description: str
    color: str
    created_at: datetime
    updated_at: datetime

    # Needed for populating the model from ORM result
    model_config = ConfigDict(from_attributes=True)
