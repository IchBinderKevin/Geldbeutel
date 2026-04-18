from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import Response

from model.schema.account import AddAccountRequest, UpdateAccountRequest, PatchAccountRequest
from service import account_service


def create_account_router() -> APIRouter:
    """
    Creates the router for account CRUD operations
    """

    router = APIRouter()

    @router.post("/add")
    async def add_account(add_account_request: AddAccountRequest):
        """
        Add a new bank account
        """
        try:
            await account_service.add_account(add_account_request)
            return Response(status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/remove/{account_id}")
    async def remove_account(account_id: int):
        """
        Removes a bank account
        """
        try:
            await account_service.remove_account(account_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/update/{account_id}")
    async def update_account(account_id: int, update_account_request: UpdateAccountRequest):
        """
        Update a bank account with the given new values
        """
        try:
            await account_service.update_account(account_id, update_account_request)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/update/{account_id}")
    async def patch_account(account_id: int, patch_account_request: PatchAccountRequest):
        """
        Patch a bank account with the given id with some new values
        """
        try:
            await account_service.patch_account(account_id, patch_account_request)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/list")
    async def list_accounts():
        """
        List all bank accounts
        """
        return await account_service.list_accounts()

    return router