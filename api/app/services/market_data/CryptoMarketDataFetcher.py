import pandas as pd
import time
from typing import List, Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.services.market_data.MarketDataAPI import MarketDataAPI
from app.services.market_data.NobitexAPI import NobitexAPI
from app.services.logger import logger


class CryptoMarketDataFetcher:
    """Main class for fetching and managing crypto market data"""

    def __init__(self):
        self.apis = {}
        self.scheduler = BackgroundScheduler()
        self.data_store = {}  # Store for the latest data
        self.price_store = {}  # Store for the latest prices

    def add_api(self, name: str, api: MarketDataAPI) -> None:
        """
        Add a new API to the fetcher

        Args:
            name (str): Name of the API
            api (MarketDataAPI): API instance
        """
        self.apis[name] = api
        logger.info(f"Added API: {name}")

    def fetch_data(
        self, api_name: str, symbols: List[str], interval: str, limit: int = 100
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple symbols from a specific API

        Args:
            api_name (str): Name of the API to use
            symbols (List[str]): List of symbols to fetch data for
            interval (str): Candlestick interval
            limit (int): Number of candles to fetch

        Returns:
            Dict[str, pd.DataFrame]: Dictionary mapping symbols to their data
        """
        if api_name not in self.apis:
            logger.error(f"API {api_name} not found")
            return {}

        api = self.apis[api_name]
        result = {}

        for symbol in symbols:
            logger.info(f"Fetching data for {symbol} from {api_name}")
            try:
                df = api.fetch_ohlc(symbol, interval, limit)
                if not df.empty:
                    result[symbol] = df
                    # Update data store
                    self.data_store[f"{api_name}_{symbol}_{interval}"] = df
                    logger.info(f"Successfully fetched data for {symbol}")
                else:
                    logger.warning(f"No data returned for {symbol}")
            except Exception as e:
                logger.error(f"Error processing {symbol}: {e}")

        return result

    def schedule_fetch(
        self,
        api_name: str,
        base_symbols: List[str],
        quote_currency: str,
        interval: str,
        limit: int = 100,
        minutes: int = 60,
    ) -> None:
        """
        Schedule regular data fetching

        Args:
            api_name (str): Name of the API to use
            base_symbols (List[str]): List of base currency symbols
            quote_currency (str): Quote currency
            interval (str): Candlestick interval
            limit (int): Number of candles to fetch
            minutes (int): Frequency of fetching in minutes
        """
        if api_name not in self.apis:
            logger.error(f"API {api_name} not found")
            return

        api = self.apis[api_name]
        symbols = api.get_symbols_format(base_symbols, quote_currency)

        # Add job to scheduler
        self.scheduler.add_job(
            func=lambda: self.fetch_data(api_name, symbols, interval, limit),
            trigger=IntervalTrigger(minutes=minutes),
            id=f"{api_name}_{quote_currency}_{interval}",
            replace_existing=True,
        )

        logger.info(
            f"Scheduled {api_name} data fetch for {symbols} every {minutes} minutes"
        )

    def start(self) -> None:
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")

    def get_latest_data(
        self, api_name: str, symbol: str, interval: str
    ) -> Optional[pd.DataFrame]:
        """
        Get the latest data for a specific symbol

        Args:
            api_name (str): Name of the API
            symbol (str): Symbol to get data for
            interval (str): Candlestick interval

        Returns:
            Optional[pd.DataFrame]: Latest data for the symbol
        """
        key = f"{api_name}_{symbol}_{interval}"
        return self.data_store.get(key)

    def fetch_latest_price(
        self, api_name: str, base_symbol: str, quote_currency: str
    ) -> Dict[str, Any]:
        """
        Fetch the latest price for a specific cryptocurrency

        Args:
            api_name (str): Name of the API to use
            base_symbol (str): Base currency symbol (e.g., 'BTC')
            quote_currency (str): Quote currency (e.g., 'USDT')

        Returns:
            Dict[str, Any]: Dictionary containing the latest price and timestamp
        """
        if api_name not in self.apis:
            logger.error(f"API {api_name} not found")
            return {
                "symbol": f"{base_symbol}/{quote_currency}",
                "price": None,
                "timestamp": None,
                "error": f"API {api_name} not found",
            }

        api = self.apis[api_name]

        try:
            price_data = api.get_latest_price(base_symbol, quote_currency)

            # Store the price data
            key = f"{api_name}_{base_symbol}_{quote_currency}"
            self.price_store[key] = price_data

            return price_data
        except Exception as e:
            logger.error(
                f"Error fetching latest price for {base_symbol}/{quote_currency} from {api_name}: {e}"
            )
            return {
                "symbol": f"{base_symbol}/{quote_currency}",
                "price": None,
                "timestamp": None,
                "error": str(e),
            }

    def schedule_price_updates(
        self,
        api_name: str,
        base_symbols: List[str],
        quote_currency: str,
        minutes: int = 1,
    ) -> None:
        """
        Schedule regular price updates

        Args:
            api_name (str): Name of the API to use
            base_symbols (List[str]): List of base currency symbols
            quote_currency (str): Quote currency
            minutes (int): Frequency of updates in minutes
        """
        if api_name not in self.apis:
            logger.error(f"API {api_name} not found")
            return

        # Add job to scheduler
        def update_prices():
            for base_symbol in base_symbols:
                self.fetch_latest_price(api_name, base_symbol, quote_currency)

        self.scheduler.add_job(
            func=update_prices,
            trigger=IntervalTrigger(minutes=minutes),
            id=f"{api_name}_prices_{quote_currency}",
            replace_existing=True,
        )

        logger.info(
            f"Scheduled {api_name} price updates for {base_symbols} every {minutes} minutes"
        )

    def get_latest_price_data(
        self, api_name: str, base_symbol: str, quote_currency: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get the latest stored price data for a specific cryptocurrency

        Args:
            api_name (str): Name of the API
            base_symbol (str): Base currency symbol
            quote_currency (str): Quote currency

        Returns:
            Optional[Dict[str, Any]]: Latest price data
        """
        key = f"{api_name}_{base_symbol}_{quote_currency}"
        return self.price_store.get(key)

    def fetch_all_now(self) -> None:
        """Execute all scheduled jobs immediately"""
        for job in self.scheduler.get_jobs():
            job.func()
        logger.info("Executed all scheduled jobs")


# Example usage
if __name__ == "__main__":
    # Create fetcher instance
    fetcher = CryptoMarketDataFetcher()

    # Add APIs
    fetcher.add_api("binance", BinanceAPI())
    fetcher.add_api(
        "cryptocompare", CryptoCompareAPI(api_key="YOUR_API_KEY")
    )  # Replace with your API key

    # Define symbols and parameters
    binance_base_symbols = ["BTC", "ETH", "SOL", "ADA"]
    cryptocompare_base_symbols = ["BTC", "ETH", "XRP", "LTC"]
    quote_currency = "USDT"
    interval = "1h"  # 1 hour candles

    # Schedule OHLC data fetching
    fetcher.schedule_fetch(
        "binance", binance_base_symbols, quote_currency, interval, limit=100, minutes=60
    )
    fetcher.schedule_fetch(
        "cryptocompare",
        cryptocompare_base_symbols,
        quote_currency,
        interval,
        limit=100,
        minutes=60,
    )

    # Schedule price updates (more frequent)
    fetcher.schedule_price_updates(
        "binance", binance_base_symbols, quote_currency, minutes=1
    )
    fetcher.schedule_price_updates(
        "cryptocompare", cryptocompare_base_symbols, quote_currency, minutes=1
    )

    # Start the scheduler
    fetcher.start()

    # For demonstration, fetch all data now
    fetcher.fetch_all_now()

    # Get latest OHLC data for a specific symbol
    binance_btc_data = fetcher.get_latest_data("binance", "BTCUSDT", "1h")
    if binance_btc_data is not None:
        print(f"Latest BTC/USDT OHLC data from Binance:\n{binance_btc_data.tail(1)}")

    # Get latest price for BTC
    binance_btc_price = fetcher.fetch_latest_price("binance", "BTC", "USDT")
    print(f"Latest BTC price from Binance: {binance_btc_price}")

    # Get latest price for ETH from CryptoCompare
    cryptocompare_eth_price = fetcher.fetch_latest_price("cryptocompare", "ETH", "USDT")
    print(f"Latest ETH price from CryptoCompare: {cryptocompare_eth_price}")

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        fetcher.stop()
