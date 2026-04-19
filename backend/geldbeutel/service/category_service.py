from datetime import datetime, UTC
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from database.db import AsyncSessionLocal
from model.domain.category import Category
from model.schema.category import AddCategoryRequest, UpdateCategoryRequest, PatchCategoryRequest, ListCategoryResponse


async def add_category(add_category_request: AddCategoryRequest):
    """
    Add a new category
    :param add_category_request: The request containing the info for the new category.
    :return: The newly created category
    """
    async with AsyncSessionLocal() as session:
        category = Category(name=add_category_request.name, icon=add_category_request.icon,
                           description=add_category_request.description, color=add_category_request.color)
        session.add(category)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError("Could not create category due to a database constraint.") from e
        await session.refresh(category)
        return category

async def remove_category(category_id: int):
    """
    Removes a category with the passed category id
    :param category_id: The id of the category to remove
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if category is None:
            raise ValueError(f"Category '{category}' does not exist.")
        try:
            await session.execute(delete(Category).where(Category.id == category_id))
            await session.commit()
            return category
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Category '{category}' cannot be removed due to a database constraint.") from e

async def update_category(category_id: int, update_category_request: UpdateCategoryRequest):
    """
    Updates a category with the passed id.
    :param category_id: The category id of the category to update
    :param update_category_request: Request containing fields to update
    :return: The updated category
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if category is None:
            raise ValueError(f"Category '{category}' does not exist.")

        category.name = update_category_request.name
        category.icon = update_category_request.icon
        category.description = update_category_request.description
        category.color = update_category_request.color
        category.updated_at = datetime.now(UTC)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Category '{category_id}' could not be updated due to a database constraint.") from e
        await session.refresh(category)
        return category

async def patch_category(category_id: int, patch_category_request: PatchCategoryRequest):
    """
    Updates a category with the passed id and only the provided values.
    :param category_id: The category id of the category to update.
    :param patch_category_request: Request containing fields to update
    :return: The updated category
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category).where(Category.id == category_id))
        category = result.scalar_one_or_none()
        if category is None:
            raise ValueError(f"Category '{category_id}' does not exist.")

        update_data = patch_category_request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                setattr(category, field, value)
        category.updated_at = datetime.now(UTC)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Category '{category_id}' could not be updated due to a database constraint.") from e
        await session.refresh(category)
        return category

async def list_categories() -> List[ListCategoryResponse]:
    """
    List all categories
    :return: List of categories
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category))
        categories = result.scalars().all()
        return [ListCategoryResponse.model_validate(a) for a in categories]
