from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.PortfolioList)
def read_portfolios(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    if crud.user.is_superuser(current_user):
        result = crud.portfolio.get_multi(db, skip=skip, limit=limit)
    else:
        result = crud.portfolio.get_multi(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return {"result": result[0], "total": result[1]}


@router.post("/", response_model=schemas.PortfolioInDBBase)
def create_portfolio(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.Portfolio,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    result = crud.portfolio.create(db=db, obj_in=obj_in, user_id=current_user.id)
    return result


@router.get("/{portfolio_id}", response_model=schemas.Portfolio)
def read_portfolio(
    *,
    db: Session = Depends(deps.get_db),
    portfolio_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    result = crud.portfolio.get_by_id(db=db, id=portfolio_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    if not crud.user.is_superuser(current_user) and (result.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return result


@router.put("/{portfolio_id}", response_model=schemas.Portfolio)
def update_portfolio(
    *,
    db: Session = Depends(deps.get_db),
    portfolio_id: int,
    obj_in: schemas.PortfolioUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    result = crud.portfolio.get_by_id(db=db, id=portfolio_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    if not crud.user.is_superuser(current_user) and (result.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    portfolio = crud.portfolio.update(db=db, db_obj=portfolio, obj_in=obj_in)
    return portfolio


@router.delete("/{portfolio_id}", response_model=schemas.Portfolio)
def delete_portfolio(
    *,
    db: Session = Depends(deps.get_db),
    portfolio_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    result = crud.portfolio.get_by_id(db=db, id=portfolio_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    if not crud.user.is_superuser(current_user) and (result.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    result = crud.portfolio.delete(db=db, db_obj=result)
    return result


@router.post("/{portfolio_id}/holdings", response_model=schemas.PortfolioHolding)
def create_portfolio_holding(
    *,
    db: Session = Depends(deps.get_db),
    portfolio_id: int,
    obj_in: schemas.PortfolioHoldingBase,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    portfolio = crud.portfolio.get_by_id(db=db, id=portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    if not crud.user.is_superuser(current_user) and (
        portfolio.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    asset = crud.asset.get_by_id(db, id=obj_in.asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    # TODO: set price_each in transaction
    transaction_in = schemas.PortfolioTransactionCreate(
        asset_id=asset.id,
        quantity=obj_in.quantity,
        price_each=0,
        portfolio_id=portfolio.id,
        price_currency_id=asset.currency_id,
        transaction_type="buy",
    )
    crud.portfolio_transaction.create(db, obj_in=transaction_in)

    same_asset_holding = crud.portfolio.get_holding_by_asset_id(
        db, portfolio_id=portfolio.id, asset_id=asset.id
    )
    if same_asset_holding:
        result = crud.portfolio.update_holding(
            db,
            db_obj=same_asset_holding,
            obj_in={"quantity": same_asset_holding.quantity + obj_in.quantity},
        )
    else:
        result = crud.portfolio.create_holding(
            db, obj_in=obj_in, portfolio_id=portfolio_id
        )

    return result


@router.get("/{portfolio_id}/holdings", response_model=List[schemas.PortfolioHolding])
def get_portfolio_holdings(
    *,
    db: Session = Depends(deps.get_db),
    portfolio_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    portfolio = crud.portfolio.get_by_id(db=db, id=portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    if not crud.user.is_superuser(current_user) and (
        portfolio.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    result = crud.portfolio.get_multi_holdings(db, portfolio_id=portfolio_id)
    for row in result:
        rate = crud.exchange_rate.get_latest_rate(
            db,
            source_currency_id=row.asset.currency_id,
            target_currency_id=portfolio.base_currency_id,
        )
        if rate:
            row.total_value = row.quantity * (rate.rate or 0)

    return result


@router.delete(
    "/{portfolio_id}/holdings/{id}", response_model=schemas.PortfolioHoldingInDBBase
)
def delete_portfolio_holding(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    portfolio_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
):
    portfolio = crud.portfolio.get_by_id(db, portfolio_id)
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found",
        )
    if not crud.user.is_superuser(current_user) and (
        portfolio.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    holding = crud.portfolio.get_holding_by_id(db, id=id)
    if not holding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio holding not found",
        )

    asset = crud.asset.get_by_id(db, id=holding.asset_id)

    # TODO: set price_each in transaction
    transaction_in = schemas.PortfolioTransactionCreate(
        asset_id=holding.asset_id,
        quantity=holding.quantity,
        price_each=0,
        portfolio_id=portfolio.id,
        price_currency_id=asset.currency_id,
        transaction_type="sell",
    )
    crud.portfolio_transaction.create(db, obj_in=transaction_in)

    result = crud.portfolio.delete_holding(db, db_obj=holding)
    return result
