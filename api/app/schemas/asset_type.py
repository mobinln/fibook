from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class AssetTypeBase(BaseModel):
    name: str
    description: Optional[str] = None


# Properties shared by models stored in DB
class AssetTypeInDBBase(AssetTypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to return via API
class AssetType(AssetTypeInDBBase):
    pass


# Properties properties stored in DB
class AssetTypeInDB(AssetTypeInDBBase):
    pass


# Properties to return for multiple assets
class AssetTypeList(BaseModel):
    result: List[AssetType]
    total: int
