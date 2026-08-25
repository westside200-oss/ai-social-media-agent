"""Account service."""

import logging
from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate

logger = logging.getLogger(__name__)


class AccountService:
    """Service for account operations."""

    async def create_account(
        self, db: Session, account_data: AccountCreate
    ) -> Account:
        """Create a new account."""
        # Check if account already exists
        existing = (
            db.query(Account)
            .filter(
                Account.platform == account_data.platform,
                Account.username == account_data.username,
            )
            .first()
        )
        
        if existing:
            raise ValueError(
                f"Account {account_data.username} already exists on {account_data.platform}"
            )
        
        account = Account(
            platform=account_data.platform,
            username=account_data.username,
            account_name=account_data.account_name,
            account_id=account_data.account_id,
            account_type=account_data.account_type,
        )
        
        # Encrypt and store tokens
        account.set_access_token(account_data.access_token)
        if account_data.refresh_token:
            account.set_refresh_token(account_data.refresh_token)
        
        db.add(account)
        db.commit()
        db.refresh(account)
        
        logger.info(f"Account created: {account.username} on {account.platform}")
        return account

    async def update_account(
        self, db: Session, account: Account, account_data: AccountUpdate
    ) -> Account:
        """Update an account."""
        if account_data.account_name:
            account.account_name = account_data.account_name
        
        if account_data.access_token:
            account.set_access_token(account_data.access_token)
        
        if account_data.refresh_token:
            account.set_refresh_token(account_data.refresh_token)
        
        if account_data.is_active is not None:
            account.is_active = account_data.is_active
        
        db.commit()
        db.refresh(account)
        
        logger.info(f"Account updated: {account.username}")
        return account
