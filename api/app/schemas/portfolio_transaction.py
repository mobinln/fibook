from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.portfolio_transaction import TransactionType
from app.schemas.currency import Currency
from app.schemas.asset import Asset


# Shared properties
class PortfolioTransactionBase(BaseModel):
    transaction_type: TransactionType
    quantity: float = Field(ge=0.0)
    price_each: float = Field(ge=0.0)
    price_currency_id: int
    notes: Optional[str] = None
    transaction_date: Optional[datetime] = None


# Properties to receive creation
class PortfolioTransactionCreate(PortfolioTransactionBase):
    portfolio_id: int
    asset_id: int


# Properties to receive update
class PortfolioTransactionUpdate(BaseModel):
    transaction_type: Optional[TransactionType] = None
    price_each: Optional[float] = Field(default=None, ge=0.0)
    quantity: Optional[float] = Field(default=None, ge=0.0)
    notes: Optional[str] = None
    transaction_date: Optional[datetime] = None


# Properties shared by models stored in DB
class PortfolioTransactionInDBBase(PortfolioTransactionBase):
    id: int
    asset_id: int
    price_currency_id: int
    portfolio_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Properties to return via API
class PortfolioTransaction(PortfolioTransactionInDBBase):
    price_currency: Currency
    asset: Asset


# Properties properties stored in DB
class PortfolioTransactionInDB(PortfolioTransactionInDBBase):
    pass


# Properties to return for multiple
class PortfolioTransactionList(BaseModel):
    result: List[PortfolioTransaction]
    total: int
