from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.portfolio_transaction.PortfolioTransactionList)
def read_portfolio_transactions(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    if crud.user.is_superuser(current_user):
        transactions = crud.portfolio_transaction.get_multi(db, skip=skip, limit=limit)
    else:
        transactions = crud.portfolio_transaction.get_multi(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return {"result": transactions[0], "total": transactions[1]}


@router.post("/", response_model=schemas.portfolio_transaction.PortfolioTransaction)
def create_portfolio_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_in: schemas.PortfolioTransactionCreate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    asset = crud.asset.get_by_id(db=db, id=transaction_in.asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Asset not found",
        )

    portfolio = crud.portfolio.get_by_id(db, transaction_in.portfolio_id)
    if not portfolio or (
        portfolio.user_id != current_user.id
        and not crud.user.is_superuser(current_user)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    holding = crud.portfolio.get_holding_by_asset_id(
        db, portfolio_id=portfolio.id, asset_id=asset.id
    )

    if holding:
        if transaction_in.transaction_type == models.TransactionType.BUY:
            crud.portfolio.update_holding(
                db,
                db_obj=holding,
                obj_in={"quantity": holding.quantity + transaction_in.quantity},
            )
        elif transaction_in.transaction_type == models.TransactionType.SALE:
            crud.portfolio.update_holding(
                db,
                db_obj=holding,
                obj_in={"quantity": holding.quantity - transaction_in.quantity},
            )
    else:
        if transaction_in.transaction_type == models.TransactionType.BUY:
            obj_in = schemas.PortfolioHoldingCreate(
                asset_id=asset.id,
                quantity=transaction_in.quantity,
                avg_purchase_price=transaction_in.price_each,
            )
            crud.portfolio.create_holding(db, portfolio_id=portfolio.id, obj_in=obj_in)

    transaction = crud.portfolio_transaction.create(
        db=db,
        obj_in=transaction_in,
    )

    return transaction


@router.get(
    "/{transaction_id}",
    response_model=schemas.portfolio_transaction.PortfolioTransaction,
)
def read_portfolio_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    transaction = crud.portfolio_transaction.get(db=db, id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    return transaction


@router.delete("/{transaction_id}", response_model=schemas.SimpleMessageResponse)
def delete_portfolio_transaction(
    *,
    db: Session = Depends(deps.get_db),
    transaction_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    transaction = crud.portfolio_transaction.get_by_id(db=db, id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    portfolio = crud.portfolio.get_by_id(db, id=transaction.portfolio_id)
    if portfolio.user_id != current_user.id and not crud.user.is_superuser(
        current_user
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    holding = crud.portfolio.get_holding_by_asset_id(
        db, portfolio_id=transaction.portfolio_id, asset_id=transaction.asset_id
    )

    if holding:
        crud.portfolio.update_holding(
            db,
            db_obj=holding,
            obj_in={"quantity": holding.quantity - transaction.quantity},
        )

    transaction = crud.portfolio_transaction.delete(db=db, db_obj=transaction)
    return {"details": "ok"}
