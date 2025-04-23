import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

from app.services.market_data.MarketDataAPI import MarketDataAPI
from app.services.logger import logger


class BinanceAPI(MarketDataAPI):
    """Binance API implementation"""

    BASE_URL = "https://api.binance.com/api/v3"

    def __init__(self):
        self.session = requests.Session()

    def get_latest_price(self, base_symbol: str, quote_currency: str) -> Dict[str, Any]:
        """
        Get the latest price of a cryptocurrency from Binance

        Args:
            base_symbol (str): Base currency symbol (e.g., 'BTC')
            quote_currency (str): Quote currency (e.g., 'USDT')

        Returns:
            Dict[str, Any]: Dictionary containing the latest price and timestamp
        """
        symbol = f"{base_symbol}{quote_currency}"
        endpoint = f"{self.BASE_URL}/ticker/price"
        params = {"symbol": symbol}

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            # For timestamp, get the server time
            time_response = self.session.get(f"{self.BASE_URL}/time")
            time_response.raise_for_status()
            server_time = time_response.json()["serverTime"]

            return {
                "symbol": symbol,
                "price": float(data["price"]),
                "timestamp": datetime.fromtimestamp(server_time / 1000),
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching latest price for {symbol}: {e}")
            return {"symbol": symbol, "price": None, "timestamp": None, "error": str(e)}

    def fetch_ohlc(self, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
        """
        Fetch OHLC data from Binance

        Args:
            symbol (str): Trading pair symbol (e.g., 'BTCUSDT')
            interval (str): Candlestick interval (e.g., '1h', '4h', '1d')
            limit (int): Number of candles to fetch (max 1000)

        Returns:
            pd.DataFrame: DataFrame containing OHLC data
        """
        endpoint = f"{self.BASE_URL}/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            df = pd.DataFrame(
                data,
                columns=[
                    "timestamp",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "quote_asset_volume",
                    "number_of_trades",
                    "taker_buy_base_asset_volume",
                    "taker_buy_quote_asset_volume",
                    "ignore",
                ],
            )

            # Convert timestamp to datetime and set as index
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df = df.set_index("timestamp")

            # Convert numeric columns to float
            numeric_columns = ["open", "high", "low", "close", "volume"]
            df[numeric_columns] = df[numeric_columns].astype(float)

            # Add symbol column
            df["symbol"] = symbol

            return df[["symbol", "open", "high", "low", "close", "volume"]]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()

    def get_symbols_format(
        self, base_symbols: List[str], quote_currency: str
    ) -> List[str]:
        """
        Format base symbols according to Binance's requirements

        Args:
            base_symbols (List[str]): List of base currency symbols (e.g., ['BTC', 'ETH'])
            quote_currency (str): Quote currency (e.g., 'USDT')

        Returns:
            List[str]: Formatted symbols (e.g., ['BTCUSDT', 'ETHUSDT'])
        """
        return [f"{base}{quote_currency}" for base in base_symbols]
