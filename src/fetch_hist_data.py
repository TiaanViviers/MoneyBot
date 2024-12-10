from dotenv import load_dotenv
import os
import sys
import requests
import pandas as pd

def fetch_daily_data(api_key, from_symbol='EUR', to_symbol='USD'):
    """
    Fetches historical daily exchange rate data for a currency pair from Polygon.io.

    Args:
        api_key (str): Polygon.io API key.
        from_symbol (str): The base currency symbol (default is 'EUR').
        to_symbol (str): The quote currency symbol (default is 'USD').

    Returns:
        pandas.DataFrame: A DataFrame containing the historical daily exchange rate data.
    """
    url = f"https://api.polygon.io/v2/aggs/ticker/C:{from_symbol}{to_symbol}/range/1/day/2014-11-23/2024-11-22"
    params = {
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch daily data: {response.status_code} {response.text}")

    data = response.json()
    if "results" not in data:
        raise ValueError("No daily data available.")

    df = pd.DataFrame(data["results"])
    df.rename(columns={
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume",
        "t": "Timestamp"
    }, inplace=True)

    df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms").dt.date
    df.set_index("Date", inplace=True)
    df.drop(columns=["Timestamp"], inplace=True)

    return df


def fetch_intraday_data(api_key, from_symbol='EUR', to_symbol='USD', interval='60'):
    """
    Fetches historical intraday exchange rate data for a currency pair from Polygon.io.

    Args:
        api_key (str): Polygon.io API key.
        from_symbol (str): The base currency symbol (default is 'EUR').
        to_symbol (str): The quote currency symbol (default is 'USD').
        interval (str): Time interval between data points (in minutes, e.g., '1', '5', '60').

    Returns:
        pandas.DataFrame: A DataFrame containing the historical intraday exchange rate data.
    """
    url = f"https://api.polygon.io/v2/aggs/ticker/C:{from_symbol}{to_symbol}/range/{interval}/minute/2014-11-23/2024-11-22"
    params = {
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch intraday data: {response.status_code} {response.text}")

    data = response.json()
    if "results" not in data:
        raise ValueError("No intraday data available.")

    df = pd.DataFrame(data["results"])
    df.rename(columns={
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume",
        "t": "Timestamp"
    }, inplace=True)

    df["Datetime"] = pd.to_datetime(df["Timestamp"], unit="ms")
    df.set_index("Datetime", inplace=True)
    df.drop(columns=["Timestamp"], inplace=True)

    return df



if __name__ == "__main__":
    # Load environment variables
    load_dotenv('../config/.env')
    api_key = os.getenv("POLYGON")
    if not api_key:
        raise ValueError("API key not found in environment variables.")

    
    if len(sys.argv) < 2:
        print("For daily data run: python3 fetch_hist_data.py daily")
        print("For intraday data run: python3 fetch_hist_data.py intraday")
    if sys.argv[1] == "daily":
        print("Fetching daily data...")
        data = fetch_daily_data(api_key)
        file_name = "../data/raw/eur_usd_daily_data.csv"
    elif sys.argv[1] == "intraday":
        print(f"Fetching intraday data with 60min interval ...")
        data = fetch_intraday_data(api_key, from_symbol='EUR', to_symbol='USD', interval='60')
        file_name = "../data/raw/eur_usd_intraday_data.csv"
    else:
        print("Invalid argument. Use 'daily' or 'intraday'.")
        sys.exit(1)

    # Save data to a CSV file
    if not data.empty:
        data.to_csv(file_name)
        print(f"Data saved to '{file_name}'")
    else:
        print(f"No data available to save for {sys.argv[1]}.")

