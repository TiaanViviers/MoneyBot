from dotenv import load_dotenv
import os
from alpha_vantage.foreignexchange import ForeignExchange


def fetch_alpha_vantage_data(api_key, from_symbol='EUR', to_symbol='USD'):
    cc = ForeignExchange(key=api_key, output_format='pandas')
    data, meta_data = cc.get_currency_exchange_daily(
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

if __name__ == "__main__":
    load_dotenv('../config/.env')
    api_key = os.getenv("ALPHA_VANTAGE")
    print(api_key)
    data = fetch_alpha_vantage_data(api_key)
    print(data.head())
    data.to_csv('../data/raw/eur_usd_data.csv')