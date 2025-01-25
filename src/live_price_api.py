import requests
import time

class LivePriceAPI:
    """
    Class to interact with Alpha Vantage for live EURUSD price readings.
    """
    def __init__(self, api_key, base_url="https://www.alphavantage.co/query", from_currency="EUR", to_currency="USD"):
        """
        Initialize the LivePriceAPI instance.

        Args:
            api_key (str): Your Alpha Vantage API key.
            base_url (str): The base URL for Alpha Vantage API.
            from_currency (str): Base currency (default is EUR).
            to_currency (str): Quote currency (default is USD).
        """
        self.api_key = api_key
        self.base_url = base_url
        self.from_currency = from_currency
        self.to_currency = to_currency

    def _get_endpoint(self):
        """
        Constructs the full URL for the API request.

        Returns:
            str: Full URL for the API request.
        """
        return (
            f"{self.base_url}?function=CURRENCY_EXCHANGE_RATE"
            f"&from_currency={self.from_currency}&to_currency={self.to_currency}&apikey={self.api_key}"
        )
    
    def get_latest_price(self):
        """
        Fetch the latest EURUSD price using the Alpha Vantage API.

        Returns:
            dict: A dictionary containing the latest price and related data.
        """
        url = self._get_endpoint()
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            try:
                exchange_rate_data = data["Realtime Currency Exchange Rate"]
                price_data = {
                    "from_currency": exchange_rate_data["1. From_Currency Code"],
                    "to_currency": exchange_rate_data["3. To_Currency Code"],
                    "exchange_rate": float(exchange_rate_data["5. Exchange Rate"]),
                    "last_refreshed": exchange_rate_data["6. Last Refreshed"],
                    "time_zone": exchange_rate_data["7. Time Zone"]
                }
                return price_data
            except KeyError:
                raise ValueError("Unexpected data format returned by the API.")
        else:
            raise ConnectionError(f"Failed to fetch data: {response.status_code}, {response.text}")


# Test client
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    
    load_dotenv('../config/.env')
    api_key = os.getenv("ALPHA_VANTAGE")
    if not api_key:
        raise ValueError("API key not found in environment variables.")
    
    price_getter = LivePriceAPI(api_key)
    while True:
        try:
            prices = price_getter.get_latest_price()
            print(prices)
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)