from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.asset import Asset


# Shared properties
class PortfolioHoldingBase(BaseModel):
    quantity: float
    asset_id: int


# Properties shared by models stored in DB
class PortfolioHoldingInDBBase(PortfolioHoldingBase):
    id: int
    portfolio_id: int
    avg_purchase_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to receive on update
class PortfolioHoldingUpdate(BaseModel):
    quantity: Optional[int] = None
    asset_id: Optional[int] = None


class PortfolioHoldingCreate(BaseModel):
    quantity: int
    asset_id: int
    avg_purchase_price: int


# Properties to return via API
class PortfolioHolding(PortfolioHoldingBase):
    id: int
    asset: Asset
    avg_purchase_price: float
    total_value: Optional[float] = None


# Properties properties stored in DB
class PortfolioHoldingInDB(PortfolioHoldingInDBBase):
    pass
