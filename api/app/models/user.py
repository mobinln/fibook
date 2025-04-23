from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    preferred_currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)

    # Relationships
    portfolios = relationship("Portfolio", back_populates="user")
    preferred_currency = relationship("Currency", foreign_keys=[preferred_currency_id])
