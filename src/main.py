from yahoo_scrape import YahooFinScrape
from trade_bot import TradeBot
import time
import sys


def main():
    if len(sys.argv) != 2:
        print("""Insufficient command line arguments!
        Please run:
            python/python3 main.py <ticker> for live prediction,
            python/python3 main.py <retrain> for automatic periodic retraining
            """)
    if sys.argv[1] == "retrain":
        print("coming soon..")
        sys.exit()
    else:
        ticker = set_ticker(sys.argv[1])
        scraper = YahooFinScrape()
        model = TradeBot()
        run_live(scraper, model, ticker)


def run_live(scraper, model, ticker):
    while True:
        data = update_data(scraper, ticker)
        prediction = model.predict(data)
        log_update(data, prediction)
        time.sleep(15)
        
        
def update_data(scraper, ticker, max_retries=3, retry_delay=5):
    """
    Fetches data for the ticker and retries on failure.

    Args:
        scraper: Your YahooFinanceScraper instance
        ticker (str): Ticker symbol
        max_retries (int): How many times to retry on failure
        retry_delay (int): Seconds to wait between retries

    Returns:
        dict or None: Ticker data if successful, or None on repeated failures
    """
    for attempt in range(1, max_retries + 1):
        try:
            data = scraper.get_ticker_data(ticker)
            return data
                
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                print("All retries failed, returning None.")
                return None
            time.sleep(retry_delay)
    

def log_update(data, prediction):
    price = data["price"]
    open = data["open_price"]
    day_high = data["day_high"]
    day_low = data["day_low"]
    #unit_diff, diff_direction = get_unit_diff(prediction, price)
    unit_diff, diff_direction = 0, 'higher/lower'
    #close_timer = get_countdown()
    close_timer = '0s'
    #pred_accuracy = get_pred_accuracy
    pred_accuracy = 0.0
    
    print("_____________________________________________________________________")
    print(f"Current Price:              {price}")
    print(f"Open Price:                 {open}")
    print(f"Daily High:                 {day_high}")
    print(f"Daily Low:                  {day_low}")
    print(f"Predicted Closing Price:    {prediction}")
    print(f"Predicted price is:         {unit_diff} {diff_direction}")
    print(f"Prediction Confidence:      {pred_accuracy}%")
    print(f"Time to Market Close:       {day_low}")
    print("_____________________________________________________________________")
    

def set_ticker(arg):
    if arg.upper() == "EURUSD" or arg.upper() == "EURUSD=X":
        return "EURUSD=X"
    elif arg.upper() == "BTCUSD" or arg.upper() == "BTC-USD":
        print("BTC-USD only supported for api testing, not prediction")
        return "BTC_USD"
    else:
        print("Ticker not currently supported. Try EURUSD")


if __name__ == "__main__":
    main()