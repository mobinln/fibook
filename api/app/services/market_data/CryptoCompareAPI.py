import requests
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.services import MarketDataAPI
from app.services.logger import logger


class CryptoCompareAPI(MarketDataAPI):
    """CryptoCompare API implementation (example of another API)"""

    BASE_URL = "https://min-api.cryptocompare.com/data"

    def __init__(self, api_key: Optional[str] = None):
        self.session = requests.Session()
        self.api_key = api_key
        if api_key:
            self.session.headers.update({"authorization": f"Apikey {api_key}"})

    def get_latest_price(self, base_symbol: str, quote_currency: str) -> Dict[str, Any]:
        """
        Get the latest price of a cryptocurrency from CryptoCompare

        Args:
            base_symbol (str): Base currency symbol (e.g., 'BTC')
            quote_currency (str): Quote currency (e.g., 'USDT')

        Returns:
            Dict[str, Any]: Dictionary containing the latest price and timestamp
        """
        endpoint = f"{self.BASE_URL}/price"
        params = {"fsym": base_symbol, "tsyms": quote_currency}

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if quote_currency not in data:
                raise ValueError(
                    f"Quote currency {quote_currency} not found in response"
                )

            # Get current timestamp since CryptoCompare price endpoint doesn't return one
            current_time = datetime.now()

            return {
                "symbol": f"{base_symbol}/{quote_currency}",
                "price": float(data[quote_currency]),
                "timestamp": current_time,
            }

        except (requests.exceptions.RequestException, ValueError) as e:
            logger.error(
                f"Error fetching latest price for {base_symbol}/{quote_currency}: {e}"
            )
            return {
                "symbol": f"{base_symbol}/{quote_currency}",
                "price": None,
                "timestamp": None,
                "error": str(e),
            }

    def fetch_ohlc(self, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
        """
        Fetch OHLC data from CryptoCompare

        Args:
            symbol (str): Trading pair symbol (e.g., 'BTC/USDT')
            interval (str): Candlestick interval (e.g., 'hour', 'day')
            limit (int): Number of candles to fetch

        Returns:
            pd.DataFrame: DataFrame containing OHLC data
        """
        # Map interval to CryptoCompare format
        interval_mapping = {
            "1m": "minute",
            "5m": "minute",
            "15m": "minute",
            "30m": "minute",
            "1h": "hour",
            "4h": "hour",
            "12h": "hour",
            "1d": "day",
            "1w": "day",
        }

        # Extract base and quote from symbol
        base, quote = symbol.split("/")

        # Determine appropriate endpoint based on interval
        if interval in ["1m", "5m", "15m", "30m"]:
            endpoint = f"{self.BASE_URL}/v2/histominute"
            # Extract the number from interval (e.g., '5m' -> 5)
            aggregate = int(interval.replace("m", ""))
        elif interval in ["1h", "4h", "12h"]:
            endpoint = f"{self.BASE_URL}/v2/histohour"
            aggregate = int(interval.replace("h", ""))
        else:  # 1d, 1w
            endpoint = f"{self.BASE_URL}/v2/histoday"
            aggregate = 1 if interval == "1d" else 7

        params = {"fsym": base, "tsym": quote, "limit": limit, "aggregate": aggregate}

        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            if data["Response"] == "Error":
                logger.error(f"API Error for {symbol}: {data['Message']}")
                return pd.DataFrame()

            df = pd.DataFrame(data["Data"]["Data"])

            # Convert timestamp to datetime and set as index
            df["timestamp"] = pd.to_datetime(df["time"], unit="s")
            df = df.set_index("timestamp")

            # Rename columns to match our standard format
            df = df.rename(
                columns={
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "volumefrom": "volume",
                }
            )

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
        Format base symbols according to CryptoCompare's requirements

        Args:
            base_symbols (List[str]): List of base currency symbols (e.g., ['BTC', 'ETH'])
            quote_currency (str): Quote currency (e.g., 'USDT')

        Returns:
            List[str]: Formatted symbols (e.g., ['BTC/USDT', 'ETH/USDT'])
        """
        return [f"{base}/{quote_currency}" for base in base_symbols]
