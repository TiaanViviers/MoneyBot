import requests
from requests.exceptions import RequestException
import time
import logging
from bs4 import BeautifulSoup


class BaseScrape:
    """
    Base class for web scrapers to handle HTTP requests and retries.
    """
    def __init__(self, headers=None, max_retries=3, retry_delay=2):
        """
        Initialize the BaseScraper.

        Args:
            headers (dict): HTTP headers for requests (e.g., user-agent).
            max_retries (int): Maximum number of retries for failed requests.
            retry_delay (int): Delay (in seconds) between retries.
        """
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        

    def fetch_html(self, url):
        """
        Fetch HTML content from a given URL with retry logic.

        Args:
            url (str): The URL to fetch.

        Returns:
            str: HTML content of the response.

        Raises:
            RequestException: If the request fails after retries.
        """
        attempts = 0
        while attempts < self.max_retries:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return response.text
            except RequestException as e:
                attempts += 1
                logging.warning(f"Request failed (attempt {attempts}/{self.max_retries}): {e}")
                time.sleep(self.retry_delay)
        
        # If all retries fail, raise an exception
        raise RequestException(f"Failed to fetch HTML after {self.max_retries} attempts: {url}")
    
    
    
class YahooFinScrape(BaseScrape):
    """
    Scraper class to extract data from Yahoo Finance for a given ticker.
    """
    def __init__(self, base_url="https://finance.yahoo.com/quote", **kwargs):
        """
        Initialize the YahooFinanceScraper.

        Args:
            base_url (str): Base URL for Yahoo Finance.
            **kwargs: Additional arguments passed to the BaseScraper.
        """
        super().__init__(**kwargs)
        self.base_url = base_url

    def _construct_url(self, ticker):
        """
        Constructs the URL for the given ticker symbol.

        Args:
            ticker (str): Ticker symbol (e.g., "BTC-USD").

        Returns:
            str: The full URL to fetch data for the ticker.
        """
        return f"{self.base_url}/{ticker}"

    def parse_ticker_data(self, html_content):
        """
        Parse the HTML content to extract relevant data.

        Args:
            html_content (str): HTML content from Yahoo Finance.

        Returns:
            dict: Parsed data including price, day high, day low, etc.
        """
        soup = BeautifulSoup(html_content, "html.parser")

        try:
            # Extract current Price
            price_tag = soup.find("span", {"data-testid": "qsp-price"})
            if not price_tag:
                raise ValueError("Could not find the price span.")
            price_text = price_tag.get_text(strip=True)
            price_value = float(price_text.replace(",", "").replace("$", ""))
            
            #Extract Day's Range
            day_range_label = soup.find("span", class_="label yf-gn3zu3", title="Day's Range")
            if day_range_label:
                range_value_span = day_range_label.find_next("span", class_="value yf-gn3zu3")
                if range_value_span:
                    range_text = range_value_span.get_text(strip=True)
                    day_low_str, day_high_str = range_text.split(" - ")

                    day_low = float(day_low_str.replace(",", ""))
                    day_high = float(day_high_str.replace(",", ""))
                else:
                    day_low, day_high = None, None
            else:
                day_low, day_high = None, None
                
            #Extract Open Price
            open_price_label = soup.find("span", class_="label yf-gn3zu3", title="Open")
            if open_price_label:
                open_price_span = open_price_label.find_next("span", class_="value yf-gn3zu3")
                if open_price_span:
                    open_price_text = open_price_span.get_text(strip=True)
                    open_price = float(open_price_text.replace(",", "").replace("$", ""))
                else:
                    open_price = None
            else:
                open_price = None

            #return scraped results
            return {
                "price": price_value,
                "day_high": day_high,
                "day_low": day_low,
                "open_price": open_price,
            }
            
        except AttributeError as e:
            logging.error(f"Error parsing HTML: {e}")
            raise ValueError("Failed to extract data from the HTML content.")

    def get_ticker_data(self, ticker):
        """
        Fetch and parse data for a given ticker symbol.

        Args:
            ticker (str): Ticker symbol (e.g., "BTC-USD").

        Returns:
            dict: Data for the ticker, including price, day high, day low, etc.
        """
        url = self._construct_url(ticker)
        html_content = self.fetch_html(url)
        return self.parse_ticker_data(html_content)
    
    
#Test client
if __name__ == "__main__":
    scraper = YahooFinScrape()

    try:
        ticker = "BTC-USD"  # Test client ticker
        data = scraper.get_ticker_data(ticker)
        print(f"Data for {ticker}: {data}")
    except Exception as e:
        print(f"Error: {e}")   