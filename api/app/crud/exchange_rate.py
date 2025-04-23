from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.schemas.exchange_rate import ExchangeRateCreate
from app.models.exchange_rate import ExchangeRate


def get_by_id(db: Session, id: int) -> Optional[ExchangeRate]:
    return db.query(ExchangeRate).filter(ExchangeRate.id == id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> Tuple[List[ExchangeRate], int]:
    query = db.query(ExchangeRate)

    total = query.count()
    result = query.offset(skip).limit(limit).all()

    return result, total


def get_latest_rate(
    db: Session, *, source_currency_id: int, target_currency_id: int
) -> ExchangeRate:
    return (
        db.query(ExchangeRate)
        .filter(ExchangeRate.source_currency_id == source_currency_id)
        .filter(ExchangeRate.target_currency_id == target_currency_id)
        .order_by(ExchangeRate.effective_date.desc())
        .first()
    )


def create(db: Session, *, obj_in: ExchangeRateCreate) -> ExchangeRate:
    db_obj = ExchangeRate(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
