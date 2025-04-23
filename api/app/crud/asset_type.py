from typing import List, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.asset_type import AssetType


def get_by_id(db: Session, id: int) -> Optional[AssetType]:
    return db.query(AssetType).filter(AssetType.id == id).first()


def get_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> Tuple[List[AssetType], int]:
    query = db.query(AssetType)

    total = query.count()
    result = query.offset(skip).limit(limit).all()

    return result, total
