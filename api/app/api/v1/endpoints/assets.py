from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.AssetList)
def read_assets(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    assets = crud.asset.get_multi(db=db, skip=skip, limit=limit)
    return {"result": assets[0], "total": assets[1]}


@router.post("/", response_model=schemas.asset.Asset)
def create_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_in: schemas.AssetCreate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new asset.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    asset = crud.asset.create(db=db, obj_in=asset_in)
    return asset


@router.get("/{asset_id}", response_model=schemas.asset.Asset)
def read_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get asset by ID.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    return asset


@router.put("/{asset_id}", response_model=schemas.asset.Asset)
def update_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    asset_in: schemas.AssetUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an asset.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    asset = crud.asset.update(db=db, db_obj=asset, obj_in=asset_in)
    return asset


@router.delete("/{asset_id}", response_model=schemas.asset.Asset)
def delete_asset(
    *,
    db: Session = Depends(deps.get_db),
    asset_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an asset.
    """
    asset = crud.asset.get(db=db, id=asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    asset = crud.asset.remove(db=db, id=asset_id)
    return asset
