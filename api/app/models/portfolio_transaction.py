from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TransactionType(str, enum.Enum):
    BUY = "buy"
    SALE = "sale"


class PortfolioTransaction(Base):
    __tablename__ = "portfolio_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(
        Float, nullable=False
    )  # quantity of asset without conversion, eg. 0.005 BTC or 10 dollars...
    price_each = Column(Float, nullable=False)
    notes = Column(String, nullable=True)

    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Foreign keys
    price_currency_id = Column(Integer, ForeignKey("currencies.id"))
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))

    # Relationships
    portfolio = relationship("Portfolio", foreign_keys=[portfolio_id])
    asset = relationship("Asset", foreign_keys=[asset_id])
    price_currency = relationship("Currency", foreign_keys=[price_currency_id])
