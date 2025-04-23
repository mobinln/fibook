from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from app.crud.exchange_rate import get_latest_rate

from app.models.portfolio import Portfolio as PortfolioModel
from app.models.portfolio_holdings import PortfolioHolding as PortfolioHoldingModel

from app.schemas.portfolio import Portfolio, PortfolioUpdate, PortfolioInDB
from app.schemas.portfolio_holding import (
    PortfolioHolding,
    PortfolioHoldingUpdate,
    PortfolioHoldingCreate,
)


def get_by_id(db: Session, id: int) -> Optional[PortfolioInDB]:
    return db.query(PortfolioModel).filter(PortfolioModel.id == id).first()


def get_multi(
    db: Session,
    *,
    user_id: Optional[int] = None,
    base_currency_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Portfolio], int]:
    query = db.query(PortfolioModel)

    if user_id is not None:
        query = query.filter(PortfolioModel.user_id == user_id)

    if base_currency_id is not None:
        query = query.filter(PortfolioModel.base_currency_id == base_currency_id)

    total = query.count()
    assets = query.offset(skip).limit(limit).all()

    return assets, total


def create(db: Session, *, obj_in: Portfolio, user_id: int) -> Portfolio:
    db_obj = PortfolioModel(**obj_in.model_dump(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Portfolio, obj_in: Union[PortfolioUpdate, Dict[str, Any]]
) -> Portfolio:
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


def update_holding(
    db: Session,
    *,
    db_obj: PortfolioHoldingModel,
    obj_in: Union[PortfolioHoldingUpdate, Dict[str, Any]]
) -> PortfolioHoldingModel:
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


def delete(db: Session, *, db_obj: PortfolioModel) -> Portfolio:
    db.delete(db_obj)
    db.commit()
    return db_obj


def get_multi_holdings(
    db: Session,
    *,
    portfolio_id: int,
    asset_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[PortfolioHolding]:
    query = db.query(PortfolioHoldingModel).filter(
        PortfolioHoldingModel.portfolio_id == portfolio_id
    )

    if asset_id:
        query = query.filter(PortfolioHoldingModel.asset_id == asset_id)

    assets = query.offset(skip).limit(limit).all()

    return assets


def get_holding_by_id(db: Session, *, id: int) -> PortfolioHolding:
    query = (
        db.query(PortfolioHoldingModel).filter(PortfolioHoldingModel.id == id).first()
    )

    return query


def get_holding_by_asset_id(
    db: Session, *, portfolio_id: int, asset_id: int
) -> PortfolioHolding:
    query = (
        db.query(PortfolioHoldingModel)
        .filter(PortfolioHoldingModel.portfolio_id == portfolio_id)
        .filter(PortfolioHoldingModel.asset_id == asset_id)
        .first()
    )

    return query


def create_holding(
    db: Session, *, obj_in: PortfolioHoldingCreate, portfolio_id: int
) -> PortfolioHoldingModel:
    db_obj = PortfolioHoldingModel(**obj_in.model_dump(), portfolio_id=portfolio_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_holding(db: Session, *, db_obj: PortfolioHoldingModel) -> PortfolioHolding:
    db.delete(db_obj)
    db.commit()
    return db_obj


def calculate_holding_total_value(
    db: Session, *, holding: PortfolioHoldingModel
) -> Optional[float]:
    rate = get_latest_rate(
        db,
        source_currency_id=holding.asset.currency_id,
        target_currency_id=holding.portfolio.base_currency_id,
    )
    if rate:
        return holding.quantity * (rate.rate or 0)

    return None
