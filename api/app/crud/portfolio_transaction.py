from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from app.models.portfolio_transaction import PortfolioTransaction
from app.schemas.portfolio_transaction import (
    PortfolioTransactionCreate,
    PortfolioTransactionUpdate,
)


def get_by_id(db: Session, id: int) -> Optional[PortfolioTransaction]:
    return db.query(PortfolioTransaction).filter(PortfolioTransaction.id == id).first()


def get_multi(
    db: Session,
    *,
    asset_id: Optional[int] = None,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> Tuple[List[PortfolioTransaction], int]:
    query = db.query(PortfolioTransaction)

    if asset_id is not None:
        query = query.filter(PortfolioTransaction.asset_id == asset_id)

    if user_id is not None:
        query = query.filter(PortfolioTransaction.portfolio.user_id == user_id)

    total = query.count()
    transactions = query.offset(skip).limit(limit).all()

    return transactions, total


def create(
    db: Session,
    *,
    obj_in: PortfolioTransactionCreate,
) -> PortfolioTransaction:
    db_obj = PortfolioTransaction(
        **obj_in.model_dump(),
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session,
    *,
    db_obj: PortfolioTransaction,
    obj_in: Union[PortfolioTransactionUpdate, Dict[str, Any]],
) -> PortfolioTransaction:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)

    for field in update_data:
        if field in update_data and update_data[field] is not None:
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, *, db_obj: PortfolioTransaction) -> PortfolioTransaction:
    db.delete(db_obj)
    db.commit()
    return db_obj
