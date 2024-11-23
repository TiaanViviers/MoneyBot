from dotenv import load_dotenv
import os
from alpha_vantage.foreignexchange import ForeignExchange

def fetch_alpha_vantage_data(api_key, from_symbol='EUR', to_symbol='USD'):
    """
    Fetches historical daily exchange rate data for a currency pair from Alpha Vantage.

    Args:
        api_key (str): Alpha Vantage API key.
        from_symbol (str): The base currency symbol (default is 'EUR').
        to_symbol (str): The quote currency symbol (default is 'USD').

    Returns:
        pandas.DataFrame: A DataFrame containing the historical exchange rate data,
                          with columns for Open, High, Low, and Close prices.
    """
    # Initialize the ForeignExchange object with API key and output format.
    cc = ForeignExchange(key=api_key, output_format='pandas')
    
    # Fetch the daily exchange rate data (full output size for entire history).
    data, meta_data = cc.get_currency_exchange_daily(
        from_symbol=from_symbol,
        to_symbol=to_symbol,
        outputsize='full'
    )
    
    # Sort by date in ascending order.
    data = data.sort_index()
    data.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close'
    }, inplace=True)
    
    return data

if __name__ == "__main__":
    load_dotenv('../config/.env')

    # Retrieve the Alpha Vantage API key from the environment variables.
    api_key = os.getenv("ALPHA_VANTAGE")
    print("Using API Key:", api_key)
    
    data = fetch_alpha_vantage_data(api_key)
    
    print(data.head())
    
    # Save the DataFrame to a CSV file in the '../data/raw' directory.
    data.to_csv('../data/raw/eur_usd_data.csv')
    print("Data saved to '../data/raw/eur_usd_data.csv'")
