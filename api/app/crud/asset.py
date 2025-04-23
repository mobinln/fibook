from typing import Any, Dict, List, Optional, Tuple, Union

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


def get_by_id(db: Session, id: int) -> Optional[Asset]:
    return db.query(Asset).filter(Asset.id == id).first()


def get_multi(
    db: Session,
    *,
    asset_type_id: Optional[int] = None,
    currency_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> Tuple[List[Asset], int]:
    query = db.query(Asset)

    if asset_type_id is not None:
        query = query.filter(Asset.asset_type_id == asset_type_id)

    if currency_id is not None:
        query = query.filter(Asset.currency_id == currency_id)

    total = query.count()
    assets = query.offset(skip).limit(limit).all()

    return assets, total


def create(db: Session, *, obj_in: AssetCreate) -> Asset:
    db_obj = Asset(**obj_in.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(
    db: Session, *, db_obj: Asset, obj_in: Union[AssetUpdate, Dict[str, Any]]
) -> Asset:
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


def delete(db: Session, *, db_obj: Asset) -> Asset:
    db.delete(db_obj)
    db.commit()
    return db_obj
