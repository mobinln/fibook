from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.currency import Currency


def get_by_id(db: Session, id: int) -> Optional[Currency]:
    return db.query(Currency).filter(Currency.id == id).first()


def get_by_code(db: Session, *, code: str) -> Currency | None:
    return db.query(Currency).filter(Currency.code == code).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> Tuple[List[Currency], int]:
    query = db.query(Currency)

    total = query.count()
    result = query.offset(skip).limit(limit).all()

    return result, total
