from datetime import datetime, UTC
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from database.db import AsyncSessionLocal
from model.domain import Account
from model.schema.account import AddAccountRequest, ListAccountResponse, UpdateAccountRequest, PatchAccountRequest


async def add_account(add_account_request: AddAccountRequest):
    """
    Add a new bank account
    :param add_account_request: The request containing the name and balance of the account to add.
    :return: The newly created account
    """
    async with AsyncSessionLocal() as session:
        account = Account(name=add_account_request.name, balance=add_account_request.balance)
        session.add(account)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError("Could not create account due to a database constraint.") from e
        await session.refresh(account)
        return account

async def remove_account(account_id: int):
    """
    Removes a bank account with the passed account id
    :param account_id: The account id of the account to remove
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        if account is None:
            raise ValueError(f"Account '{account_id}' does not exist.")
        try:
            await session.execute(delete(Account).where(Account.id == account_id))
            await session.commit()
            return account
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Account '{account_id}' cannot be removed due to a database constraint.") from e

async def update_account(account_id: int, update_account_request: UpdateAccountRequest):
    """
    Updates a bank account with the passed id.
    :param account_id: The account id of the account to update
    :param update_account_request: Request containing fields to update
    :return: The updated account
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        if account is None:
            raise ValueError(f"Account '{account_id}' does not exist.")

        account.name = update_account_request.name
        account.balance = update_account_request.balance
        account.updated_at = datetime.now(UTC)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Account '{account_id}' could not be updated due to a database constraint.") from e
        await session.refresh(account)
        return account

async def patch_account(account_id: int, patch_account_request: PatchAccountRequest):
    """
    Updates a bank account with the passed id and only the provided values
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        if account is None:
            raise ValueError(f"Account '{account_id}' does not exist.")

        update_data = patch_account_request.model_dump(exclude_unset=True)

        for field, value in update_data.items():
                setattr(account, field, value)
        account.updated_at = datetime.now(UTC)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            raise ValueError(f"Account '{account_id}' could not be updated due to a database constraint.") from e
        await session.refresh(account)
        return account

async def list_accounts() -> List[ListAccountResponse]:
    """
    List all accounts
    :return: List of accounts
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Account))
        accounts = result.scalars().all()
        return [ListAccountResponse.model_validate(a) for a in accounts]
