import pandas_datareader as pdr # access fred
import pandas as pd
import requests # data from api
# import plotly.express as px # visualize
from datetime import datetime


def fetch_fred_data_as_df(series_id,api_key):
    """
    Fetches data for a given series ID from the FRED API and returns as a pandas DataFrame.

    Args:
    - series_id (str): The series ID of the economic indicator.

    Returns:
    - pandas.DataFrame: DataFrame containing the fetched data.
    """
    base_url = "https://api.stlouisfed.org/fred/"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }

    response = requests.get(base_url + "series/observations", params=params)
    data = response.json()['observations']
    # Convert JSON data to pandas DataFrame
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df

api_key = "fb97ce177d1337f7c67916562b9a164a"
df_gdp = fetch_fred_data_as_df("GDP", api_key)
df_cpi = fetch_fred_data_as_df("CPIAUCSL", api_key)
df_unemployment = fetch_fred_data_as_df("UNRATE", api_key)
df_interest_rate = fetch_fred_data_as_df("DFF", api_key)
df_stock_index = fetch_fred_data_as_df("SP500", api_key)