"""API routes for account management."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.services.account_service import AccountService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/accounts", tags=["accounts"])
service = AccountService()


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db),
):
    """Create a new social media account."""
    try:
        account = await service.create_account(db, account_data)
        return account
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=List[AccountResponse])
async def list_accounts(
    platform: str = None,
    is_active: bool = True,
    db: Session = Depends(get_db),
):
    """List all accounts, optionally filtered by platform."""
    query = db.query(Account).filter(Account.is_active == is_active)
    
    if platform:
        query = query.filter(Account.platform == platform)
    
    accounts = query.all()
    return accounts


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific account by ID."""
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    
    return account


@router.patch("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account_data: AccountUpdate,
    db: Session = Depends(get_db),
):
    """Update account details."""
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    
    try:
        updated_account = await service.update_account(db, account, account_data)
        return updated_account
    except Exception as e:
        logger.error(f"Error updating account: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
):
    """Soft delete an account (mark as inactive)."""
    account = db.query(Account).filter(Account.id == account_id).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
    
    account.is_active = False
    db.commit()
    return None
