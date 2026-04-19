from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response

from model.schema.account import AddAccountRequest, UpdateAccountRequest, PatchAccountRequest
from model.schema.category import AddCategoryRequest, UpdateCategoryRequest, PatchCategoryRequest
from service import account_service, category_service


def create_category_router() -> APIRouter:
    """
    Creates the router for category CRUD operations
    """

    router = APIRouter()

    @router.post("/add")
    async def add_category(add_category_request: AddCategoryRequest):
        """
        Add a new category
        """
        try:
            await category_service.add_category(add_category_request)
            return Response(status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/remove/{category_id}")
    async def remove_category(category_id: int):
        """
        Removes a category with the given id
        """
        try:
            await category_service.remove_category(category_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/update/{category_id}")
    async def update_category(category_id: int, update_category_request: UpdateCategoryRequest):
        """
        Update a category with the given new values
        """
        try:
            await category_service.update_category(category_id, update_category_request)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/update/{category_id}")
    async def patch_category(category_id: int, patch_category_request: PatchCategoryRequest):
        """
        Patch a category with the given id with some new values
        """
        try:
            await category_service.patch_category(category_id, patch_category_request)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/list")
    async def list_categories():
        """
        List all categories
        """
        return await category_service.list_categories()

    return router