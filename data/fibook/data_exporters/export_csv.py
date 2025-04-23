from mage_ai.io.file import FileIO
from pandas import DataFrame
from datetime import datetime, timedelta

if "data_exporter" not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


def get_date_range_string():
    today = datetime.today().date()
    thirty_days_ago = today - timedelta(days=30)
    today_str = today.strftime("%Y-%m-%d")
    thirty_days_ago_str = thirty_days_ago.strftime("%Y-%m-%d")

    return f"{thirty_days_ago_str}-{today_str}"


@data_exporter
def export_data_to_file(df: DataFrame, **kwargs) -> None:
    date = get_date_range_string()
    filepath = f"crypto_market_{date}.csv"
    FileIO().export(df, filepath)
