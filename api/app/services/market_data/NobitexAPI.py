import time
import requests
import pandas as pd
import numpy as np
from typing import Dict, Any

from app.services.market_data.MarketDataAPI import MarketDataAPI
from app.services.logger import logger


class NobitexAPI(MarketDataAPI):
    BASE_URL = "https://api.nobitex.ir"

    def __init__(self):
        self.session = requests.Session()

    def get_latest_price(self, base_symbol: str, quote_currency: str) -> Dict[str, Any]:
        symbol = f"{base_symbol}{quote_currency}"
        endpoint = f"{self.BASE_URL}/market/udf/history"
        ts = time.time()
        params = {
            "symbol": symbol,
            "resolution": "1",
            "from": int(ts - 5 * 60),
            "to": int(ts + 50 * 60),
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            df = df.sort_values(by="t", ascending=False)
            df["t"] = pd.to_datetime(df["t"], unit="s")
            df["t"] = df["t"].dt.tz_localize("UTC")
            df["t"] = df["t"].dt.tz_convert("Asia/Tehran")

            price_row = df.iloc[0]

            return {
                "symbol": symbol,
                "price": np.average([price_row["h"], price_row["l"]]),
                "timestamp": price_row["t"],
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching latest price for {symbol}: {e}")
            return {"symbol": symbol, "price": None, "timestamp": None, "error": str(e)}

    def fetch_ohlc(self, symbol: str, interval: str, limit: int = 10) -> pd.DataFrame:
        endpoint = f"{self.BASE_URL}/market/udf/history"
        ts = time.time()
        params = {
            "symbol": symbol,
            "resolution": interval,
            "from": int(ts) - 8 * 60 * 60,
            "to": int(ts) + 60,
            "countback": limit,
        }

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(data)
            df.columns = [
                "status",
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
            df = df.sort_values(by="timestamp", ascending=True)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            df["timestamp"] = df["timestamp"].dt.tz_localize("UTC")
            df["timestamp"] = df["timestamp"].dt.tz_convert("Asia/Tehran")
            df = df.set_index("timestamp")

            numeric_columns = ["open", "high", "low", "close", "volume"]
            df[numeric_columns] = df[numeric_columns].astype(float)

            df["symbol"] = symbol
            df = df.drop(["status"], axis=1)

            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching latest price for {symbol}: {e}")
            return {"symbol": symbol, "price": None, "timestamp": None, "error": str(e)}
