from dotenv import load_dotenv
import os
import sys
import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange


def get_hist_data(file_name, symbol):
    """
    Fetches and updates historical data for a given symbol.

    This function checks if the specified file containing historical data exists. If the file exists,
    it fetches new data starting from the last date present in the file and appends it
    to the existing data. If the file does not exist, it fetches the full historical data
    and saves it to a new file. Currently, only the EURUSD symbol is supported.

    Args:
        file_name (str): The name of the file (excluding the path) to save or update with historical data. 
                        It is assumed to be located in the "../data/raw/" directory.
        symbol (str): The trading symbol (e.g., 'EURUSD') for which to fetch historical data.

    Returns:
        None

    Notes:
        - The function is designed specifically for Alpha Vantage's API structure and assumes 
        supporting functions (`load_env`, `file_exists`, `read_last_date`, `fetch_alpha_vantage_data`, 
        and `save_csv`) are available in the module.
        - The `EURUSD` symbol is case-insensitive.
"""
    api_key = load_env()
    print(file_exists(file_name))
    if file_exists(file_name):
        if symbol.upper() == 'EURUSD':
            last_date = read_last_date(file_name)
            data = fetch_alpha_vantage_data(api_key, symbol, last_date)
            save_csv(file_name, data, append=True)
            return
        
        else:
            print("Symbol is currently not supported, sorry!")
            sys.exit()
    
    else:
        if symbol.upper() == 'EURUSD':
            data = fetch_alpha_vantage_data(api_key, symbol)
            save_csv(file_name, data)
            return
        else:
            print("Symbol is currently not supported, sorry!")
            sys.exit()


def fetch_alpha_vantage_data(api_key, symbol, from_date=None):
    """
    Fetches historical daily exchange rate data for a currency pair from Alpha Vantage.

    Args:
        api_key (str): Alpha Vantage API key.
        symbol (str): The currency pair symbol (e.g., 'EURUSD').
        from_date (str, optional): The start date (inclusive) for fetching data in 'YYYY-MM-DD' format.
                                   If None, fetches all available historical data.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical exchange rate data,
                          with columns for Open, High, Low, and Close prices, starting from `from_date` (if provided).
    """
    if symbol.upper() == 'EURUSD':
        from_symbol = 'EUR'
        to_symbol = 'USD'
    else:
        print("Symbol not currently supported, sorry!")
        sys.exit()
    
    cc = ForeignExchange(key=api_key, output_format='pandas')
    data, meta_data = cc.get_currency_exchange_daily(
        from_symbol=from_symbol,
        to_symbol=to_symbol,
        outputsize='full'
    )

    # Sort by date
    data = data.sort_index()
    data.rename(columns={
        '1. open': 'Open',
        '2. high': 'High',
        '3. low': 'Low',
        '4. close': 'Close'
    }, inplace=True)

    # If from_date is provided, filter data
    if from_date:
        data = data.loc[from_date:]  # Include data starting from from_date
        if not data.empty:
            data = data.iloc[1:]  # Remove the first entry (duplicate)

    return data


def read_last_date(filename):
    """
    Reads the last date entry from a CSV file.

    Args:
        filename (str): Name of the file (without extension) to read from, located in '../data/raw/'.

    Returns:
        str: The last date in the file as a string in the format 'YYYY-MM-DD', or None if the file is empty.
    """
    file_path = f"../data/raw/{filename}.csv"
    data = pd.read_csv(file_path)
    
    # Load the CSV file
    if data.empty:
        print("No data in provided filename, please remove empty file in ../data/raw/ dir and try again.")
        sys.exit()
    
    # Access the last row of the first column
    last_date = data.iloc[-1, 0]
    return last_date
    

def file_exists(file_name):
    """
    Check if a file exists in the '../data/raw/' directory.

    Args:
        file_name (str): Name of the file to check (e.g., 'eur_usd_data.csv').

    Returns:
        bool: True if the file exists, False otherwise.
    """
    file_path = file_path = f"../data/raw/{file_name}.csv"
    return os.path.exists(file_path)


def load_env():
    """
    Function that loads the .env file and extracts the api key used to retrieve 
    the historical data from Alpha Vantage.

    Returns:
        api_key: the api key used to access the Alpha Vantage historical data
    """
    load_dotenv('../config/.env')
    api_key = os.getenv("ALPHA_VANTAGE")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    
    return api_key


def save_csv(file_name, data, append=None):
    """
    Saves the given data to a CSV file. Appends to the file if specified, otherwise
    creates a new file.

    Args:
        file_name (str): The name of the file (without extension) to save the data to.
        data (pandas.DataFrame): The data to be saved.
        append (bool, optional): If True, appends the data to the file. 
                                 If False, creates a new file. Default is False.

    Returns:
        None
    """
    file_path = f"../data/raw/{file_name}.csv"

    if append:
        # Append to the file
        data.to_csv(file_path, mode='a', header=False, index=True)
        print(f"Data appended to {file_path}")
    else:
        # Create a new file or overwrite the existing one
        data.to_csv(file_path, mode='w', header=True, index=True)
        print(f"Data saved to {file_path}")
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("""Insufficient command line arguments!
        Please provide command line arguments in this format:
                    1- filename data must be saved to, e.g. eur_usd_data
                    2- Symbol/ticker e.g. EURUSD
            """)
        sys.exit()
    
    else:
        file_name = sys.argv[1]
        symbol = sys.argv[2]
        get_hist_data(file_name, symbol)
