from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.services.market_data.NobitexAPI import NobitexAPI
from app.core.database import SessionLocal
from app import crud, schemas


def get_crypto_prices():
    exchange_rules = [
        {"source": "BTC", "target": "USDT"},
        {"source": "BTC", "target": "IRT"},
        {"source": "ETH", "target": "USDT"},
        {"source": "ETH", "target": "IRT"},
        {"source": "USDT", "target": "IRT"},
    ]
    nobitex_api = NobitexAPI()

    for rule in exchange_rules:
        with SessionLocal() as db:
            result = nobitex_api.get_latest_price(
                base_symbol=rule["source"],
                quote_currency=rule["target"],
            )
            source_currency = crud.currency.get_by_code(db, code=rule["source"])
            target_currency = crud.currency.get_by_code(db, code=rule["target"])

            obj = schemas.ExchangeRateCreate(
                rate=result["price"],
                effective_date=result["timestamp"],
                source_currency_id=source_currency.id,
                target_currency_id=target_currency.id,
            )
            crud.exchange_rate.create(db, obj_in=obj)


def get_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=get_crypto_prices,
        trigger=IntervalTrigger(minutes=10),
        id=f"crypto_nobitex_1",
        replace_existing=True,
    )

    return scheduler
