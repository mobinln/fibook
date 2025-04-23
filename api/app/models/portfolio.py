from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"))
    base_currency_id = Column(Integer, ForeignKey("currencies.id"))

    # Relationships
    user = relationship("User", back_populates="portfolios")
    base_currency = relationship("Currency")
    holdings = relationship(
        "PortfolioHolding", back_populates="portfolio", cascade="all, delete-orphan"
    )
