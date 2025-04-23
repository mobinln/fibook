from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.asset_type import AssetType
from app.schemas.currency import Currency


# Shared properties
class AssetBase(BaseModel):
    name: str
    symbol: str
    description: Optional[str] = None
    is_active: bool
    asset_type_id: int
    currency_id: int


# Properties to receive on asset creation
class AssetCreate(AssetBase):
    pass


# Properties to receive on asset update
class AssetUpdate(BaseModel):
    name: Optional[str] = None
    symbol: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    asset_type_id: Optional[int] = None
    currency_id: Optional[int] = None


# Properties shared by models stored in DB
class AssetInDBBase(AssetBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to return via API
class Asset(AssetInDBBase):
    asset_type: AssetType
    currency: Currency


# Properties properties stored in DB
class AssetInDB(AssetInDBBase):
    pass


# Properties to return for multiple assets
class AssetList(BaseModel):
    result: List[Asset]
    total: int
