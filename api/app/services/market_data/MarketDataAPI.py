import pandas as pd
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class MarketDataAPI(ABC):
    """Abstract base class for market data APIs"""

    @abstractmethod
    def fetch_ohlc(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        """
        Fetch OHLC data for a given symbol

        Args:
            symbol (str): Trading pair symbol
            interval (str): Candlestick interval
            limit (int): Number of candles to fetch

        Returns:
            pd.DataFrame: DataFrame containing OHLC data
        """
        pass

    @abstractmethod
    def get_latest_price(self, base_symbol: str, quote_currency: str) -> Dict[str, Any]:
        """
        Get the latest price of a cryptocurrency

        Args:
            base_symbol (str): Base currency symbol (e.g., 'BTC')
            quote_currency (str): Quote currency (e.g., 'USDT')

        Returns:
            Dict[str, Any]: Dictionary containing the latest price and timestamp
                            {
                                'symbol': str,
                                'price': float,
                                'timestamp': datetime
                            }
        """
        pass
