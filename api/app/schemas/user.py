from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.schemas.currency import CurrencyInDBBase


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    is_superuser: Optional[bool] = False


# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    preferred_currency_id: Optional[int] = None


# Properties shared by models stored in DB
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None


# Properties to return via API
class User(UserBase):
    id: int
    preferred_currency: CurrencyInDBBase

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    result: List[User]
    total: int


# Properties properties stored in DB
class UserInDB(UserBase):
    id: int
    hashed_password: str
    preferred_currency_id: Optional[int] = None

    class Config:
        from_attributes = True
