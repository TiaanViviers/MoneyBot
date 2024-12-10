from dotenv import load_dotenv
import os
import sys
from alpha_vantage.foreignexchange import ForeignExchange
import pandas as pd

def fetch_daily_data(api_key, from_symbol='EUR', to_symbol='USD'):
    """
    Fetches historical daily exchange rate data for a currency pair from Alpha Vantage.

    Args:
        api_key (str): Alpha Vantage API key.
        from_symbol (str): The base currency symbol (default is 'EUR').
        to_symbol (str): The quote currency symbol (default is 'USD').

    Returns:
        pandas.DataFrame: A DataFrame containing the historical daily exchange rate data.
    """
    cc = ForeignExchange(key=api_key, output_format='pandas')
    data, _ = cc.get_currency_exchange_daily(
        from_symbol=from_symbol,
        to_symbol=to_symbol,
        outputsize='full'
    )
    data = data.sort_index()
    data.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close'
    }, inplace=True)
    return data


def fetch_intraday_data(api_key, from_symbol='EUR', to_symbol='USD', interval='60min'):
    """
    Fetches historical intraday exchange rate data for a currency pair from Alpha Vantage.

    Args:
        api_key (str): Alpha Vantage API key.
        from_symbol (str): The base currency symbol (default is 'EUR').
        to_symbol (str): The quote currency symbol (default is 'USD').
        interval (str): Time interval between data points (e.g., '1min', '5min', '60min').

    Returns:
        pandas.DataFrame: A DataFrame containing the historical intraday exchange rate data.
    """
    cc = ForeignExchange(key=api_key, output_format='pandas')
    data, _ = cc.get_currency_exchange_intraday(
        from_symbol=from_symbol,
        to_symbol=to_symbol,
        interval=interval,
        outputsize='full'
    )
    data = data.sort_index()
    data.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close',
        '5. volume': 'Volume'
    }, inplace=True)
    return data


if __name__ == "__main__":
    # Load environment variables
    load_dotenv('../config/.env')
    api_key = os.getenv("ALPHA_VANTAGE")
    if not api_key:
        raise ValueError("API key not found in environment variables. Please check your .env file.")

    
    if len(sys.argv) < 2:
        print("For daily data run: python3 fetch_hist_data.py daily")
        print("For intraday data run: python3 fetch_hist_data.py intraday")
        
    if sys.argv[1] == "daily":
        print("Fetching daily data...")
        data = fetch_daily_data(api_key)
        file_name = "../data/eur_usd_daily_data.csv"
    elif sys.argv[1] == "intraday":
        print(f"Fetching intraday data with 60min interval ...")
        data = fetch_intraday_data(api_key)
        file_name = "eur_usd_intraday_data.csv"

    # Save data to a CSV file
    data.to_csv(file_name)
    print(f"Data saved to '{file_name}'")
