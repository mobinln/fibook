from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class CurrencyBase(BaseModel):
    name: str
    code: str
    symbol: str
    is_fiat: bool


# Properties shared by models stored in DB
class CurrencyInDBBase(CurrencyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to return via API
class Currency(CurrencyInDBBase):
    pass


# Properties properties stored in DB
class CurrencyInDB(CurrencyInDBBase):
    pass


# Properties to return for multiple assets
class CurrencyList(BaseModel):
    result: List[Currency]
    total: int
