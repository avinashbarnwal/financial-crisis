import pandas_datareader as pdr # access fred
import pandas as pd
import requests # data from api
# import plotly.express as px # visualize
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np

def get_plots(df,plot_name):
    df['value']=df['value']
    # df_gdp['value']=df_gdp['value'].apply(lambda x: x.replace('.',''))

    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df=df[~df['value'].isna()]

    df=df.reset_index()
    df['date']=pd.to_datetime(df['date'],format='%Y-%m-%d', errors='coerce')
    df['date']=df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['date']=df['date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))



    df=df.reset_index(drop=True)
    # df_gdp['value']=df_gdp['value'].astype(float)
    plt.ioff()
    plt.plot(df['date'],df['value'])
    plt.savefig(plot_name)
    plt.xticks(rotation=45)
    plt.close()

    # df_gdp.to_csv("gdp.csv")

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

get_plots(df_gdp,'gdp.png')
get_plots(df_cpi,'cpi.png')
get_plots(df_unemployment,'unemployment.png')
get_plots(df_interest_rate,'interest_rate.png')
get_plots(df_stock_index,'stock.png')