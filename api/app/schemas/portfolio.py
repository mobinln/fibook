from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool
    base_currency_id: int


# Properties shared by models stored in DB
class PortfolioInDBBase(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to receive on update
class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    base_currency_id: Optional[int] = None


# Properties to return via API
class Portfolio(PortfolioBase):
    pass


# Properties properties stored in DB
class PortfolioInDB(PortfolioInDBBase):
    pass


# Properties to return for multiple assets
class PortfolioList(BaseModel):
    result: List[PortfolioInDB]
    total: int
