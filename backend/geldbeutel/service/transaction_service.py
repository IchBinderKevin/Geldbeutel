from datetime import datetime, UTC
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from database.db import AsyncSessionLocal
from model.domain import Transaction
from model.schema.transaction import (AddTransactionModel, UpdateTransactionRequest,
                                      PatchTransactionRequest, ListTransactionResponse)


async def add_transaction(add_transaction_request: AddTransactionModel):
    """
    Add a new transaction
    :param add_transaction_request: The request containing the info for the new transaction.
    :return: The newly created category
    """
    async with AsyncSessionLocal() as session:
        transaction = Transaction(title=add_transaction_request.title, amount=add_transaction_request.amount,
                           date=add_transaction_request.date, type=add_transaction_request.type,
                               category_id=add_transaction_request.category_id)
        session.add(transaction)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            print(e)
            raise ValueError("Could not create transaction due to a database constraint.") from e
        await session.refresh(transaction)
        return transaction

async def remove_transaction(transaction_id: int):
    """
    Removes a transaction with the passed transaction id
    :param transaction_id: The id of the transaction to remove
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise ValueError(f"Transaction '{transaction_id}' does not exist.")
        try:
            await session.execute(delete(Transaction).where(Transaction.id == transaction_id))
            await session.commit()
            return transaction
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Transaction '{transaction_id}' cannot be removed due to a database constraint.") from e

async def update_transaction(transaction_id: int, update_transaction_request: UpdateTransactionRequest):
    """
    Updates a transaction with the passed id.
    :param transaction_id: The transaction id of the transaction to update
    :param update_transaction_request: Request containing fields to update
    :return: The updated transaction
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise ValueError(f"Transaction '{transaction_id}' does not exist.")

        transaction.title = update_transaction_request.title
        transaction.amount = update_transaction_request.amount
        transaction.date = update_transaction_request.date
        transaction.type = update_transaction_request.type
        transaction.category_id = update_transaction_request.category_id
        transaction.updated_at = datetime.now(UTC)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Transaction '{transaction_id}' could not be updated due to a database constraint.") from e
        await session.refresh(transaction)
        return transaction

async def patch_transaction(transaction_id: int, patch_transaction_request: PatchTransactionRequest):
    """
    Updates a transaction with the passed id and only the provided values.
    :param transaction_id: The transaction id of the transaction to update.
    :param patch_transaction_request: Request containing fields to update
    :return: The updated transaction
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Transaction).where(Transaction.id == transaction_id))
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise ValueError(f"Transaction '{transaction_id}' does not exist.")

        update_data = patch_transaction_request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                setattr(transaction, field, value)
        transaction.updated_at = datetime.now(UTC)

        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Transaction '{transaction_id}' could not be updated due to a database constraint.") from e
        await session.refresh(transaction)
        return transaction

async def list_transactions(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
) -> List[ListTransactionResponse]:
    """
    List transactions, optionally filtered by a date range.
    :return: List of transactions
    """
    if (start_date is None) != (end_date is None):
        raise ValueError("Both start_date and end_date must be provided together.")

    if start_date is not None and end_date is not None and start_date > end_date:
        raise ValueError("start_date must be less than or equal to end_date.")

    async with AsyncSessionLocal() as session:
        query = select(Transaction)

        if start_date is not None and end_date is not None:
            query = query.where(Transaction.date >= start_date, Transaction.date <= end_date)

        result = await session.execute(query)
        transactions = result.scalars().all()
        return [ListTransactionResponse.model_validate(t) for t in transactions]
