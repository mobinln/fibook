from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    currency_id = Column(Integer, ForeignKey("currencies.id"))

    # Relationships
    asset_type = relationship("AssetType", foreign_keys=[asset_type_id])
    currency = relationship("Currency", foreign_keys=[currency_id])
