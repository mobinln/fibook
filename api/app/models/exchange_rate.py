from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    rate = Column(Float, nullable=False, default=0)
    effective_date = Column(DateTime(timezone=True), server_default=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    source_currency_id = Column(Integer, ForeignKey("currencies.id"))
    target_currency_id = Column(Integer, ForeignKey("currencies.id"))

    # Relationships
    source_currency = relationship("Currency", foreign_keys=[source_currency_id])
    target_currency = relationship("Currency", foreign_keys=[target_currency_id])
