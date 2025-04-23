from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Boolean,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TimeFrame(str, enum.Enum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"
    ONE_WEEK = "1w"


class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime(timezone=True), server_default=func.now())
    timeframe = Column(Enum(TimeFrame), nullable=False)
    open_price = Column(Float, nullable=False, default=0)
    close_price = Column(Float, nullable=False, default=0)
    high_price = Column(Float, nullable=False, default=0)
    low_price = Column(Float, nullable=False, default=0)
    volume = Column(Float, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    asset_id = Column(Integer, ForeignKey("assets.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))

    # Relationships
    asset = relationship("Asset", foreign_keys=[asset_id])
    currency = relationship("Currency", foreign_keys=[currency_id])
