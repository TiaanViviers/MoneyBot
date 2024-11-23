import yfinance as yf

def fetch_hist_data(symbol, start_date, end_date, interval="1d"):
    """
    Fetch historical price data for a given symbol using Yahoo Finance.

    Args:
        symbol (str): Ticker symbol (e.g., 'EURUSD=X' for Forex).
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        interval (str): Data interval ('1d', '1h', '5m', etc.).

    Returns:
        pd.DataFrame: Dataframe containing price data.
    """
    print(f"Fetching data for {symbol} from {start_date} to {end_date}...")
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    return data

if __name__ == "__main__":
    # Params to fetch daily data
    symbol = "EURUSD=X"
    start_date = "2015-01-01"
    end_date = "2024-11-23"
    interval = "1d"

    data = fetch_hist_data(symbol, start_date, end_date, interval)

    # Save to CSV
    output_file = "../data/raw/eur_usd_data.csv"
    data.to_csv(output_file)
    print(f"Data saved to {output_file}")