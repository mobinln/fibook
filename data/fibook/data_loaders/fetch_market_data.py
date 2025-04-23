import io
import pandas as pd
import requests
from datetime import datetime, timedelta, time, timezone

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def get_day_range_timestamps():
    now = datetime.now(timezone.utc)
    end_of_today = now.replace(hour=23, minute=59, second=59, microsecond=0)
    start_of_30_days_ago = (now - timedelta(days=30)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    return int(start_of_30_days_ago.timestamp()), int(end_of_today.timestamp())


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    symbols = ["BTCIRT", "USDTIRT", "ETHIRT", "BCHUSDT", "ETHUSDT"]
    start_ts, end_ts = get_day_range_timestamps()
    url = "https://api.nobitex.ir/market/udf/history"

    final_df = pd.DataFrame()

    for s in symbols:
        params = {
            "symbol": s,
            "resolution": "60",
            "from": start_ts,
            "to": end_ts,
            "page": 1,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)

        df["symbol"] = s
        df = df.drop(["s"], axis=1)

        final_df = pd.concat([final_df, df], axis=0)

    return final_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
    assert output.shape[0] > 0, "The output has some rows"
    assert output.shape[1] > 0, "The output has some columns"
