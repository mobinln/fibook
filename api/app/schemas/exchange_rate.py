from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ExchangeRateBase(BaseModel):
    rate: float
    effective_date: datetime


class ExchangeRateCreate(ExchangeRateBase):
    source_currency_id: int
    target_currency_id: int
