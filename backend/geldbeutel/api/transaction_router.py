from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, HTTPException, Query
from starlette import status
from starlette.responses import Response

from model.schema.transaction import AddTransactionModel, UpdateTransactionRequest, PatchTransactionRequest
from service import transaction_service


def create_transaction_router() -> APIRouter:
    """
    Creates the router for transaction CRUD operations
    """

    router = APIRouter()

    @router.post("/add")
    async def add_transaction(add_transaction_request: AddTransactionModel):
        """
        Add a new transaction
        """
        try:
            await transaction_service.add_transaction(add_transaction_request)
            return Response(status_code=status.HTTP_201_CREATED)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/remove/{transaction_id}")
    async def remove_transaction(transaction_id: int):
        """
        Removes a transaction with the given id
        """
        try:
            await transaction_service.remove_transaction(transaction_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put("/update/{transaction_id}")
    async def update_transaction(transaction_id: int, update_transaction_request: UpdateTransactionRequest):
        """
        Update a transaction with the given new values
        """
        try:
            await transaction_service.update_transaction(transaction_id, update_transaction_request)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.patch("/update/{transaction_id}")
    async def patch_transaction(transaction_id: int, patch_transaction_request: PatchTransactionRequest):
        """
        Patch a transaction with the given id with some new values
        """
        try:
            await transaction_service.patch_transaction(transaction_id, patch_transaction_request)
            return Response(status_code=status.HTTP_200_OK)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/list")
    async def list_transactions(
        start_date: Annotated[Optional[datetime], Query()] = None,
        end_date: Annotated[Optional[datetime], Query()] = None,
    ):
        """
        List all transactions, optionally filtered by date range.
        Dates must be in ISO 8601 format, e.g. 2026-04-01T00:00:00
        """
        try:
            return await transaction_service.list_transactions(start_date=start_date, end_date=end_date)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router