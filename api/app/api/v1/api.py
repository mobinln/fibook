"""API router for v1 endpoints."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    portfolio_transactions,
    users,
    assets,
    asset_type,
    currency,
    portfolio,
)

api_router = APIRouter()

# Include all API routers with appropriate prefixes and tags
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(
    asset_type.router, prefix="/asset-types", tags=["asset-types"]
)
api_router.include_router(currency.router, prefix="/currencies", tags=["currencies"])
api_router.include_router(
    portfolio_transactions.router,
    prefix="/portfolio-transactions",
    tags=["portfolio-transactions"],
)
api_router.include_router(portfolio.router, prefix="/portfolios", tags=["portfolios"])
