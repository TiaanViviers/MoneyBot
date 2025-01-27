from yahoo_scrape import YahooFinScrape
from trade_bot import TradeBot
from periodic_retrain import retrain
import time
import sys
from datetime import datetime
from zoneinfo import ZoneInfo


def main():
    if len(sys.argv) != 2:
        print("""Insufficient command line arguments!
        Please run:
            python/python3 main.py <ticker> for live prediction,
            python/python3 main.py <retrain> for automatic model retraining
            """)
    if sys.argv[1].lower() == "retrain":
        retrain()
        sys.exit()
    else:
        ticker = set_ticker(sys.argv[1])
        scraper = YahooFinScrape()
        model = TradeBot()
        run_live(scraper, model, ticker)


def run_live(scraper, model, ticker):
    while True:
        data = update_data(scraper, ticker)
        close_timer = get_countdown()
        prediction = model.predict(data)
        pred_accuracy = model.pred_confidence(close_timer)
        log_update(data, close_timer, prediction, pred_accuracy)
        time.sleep(180)
        
        
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
    

def get_countdown():
    """
    Calculates time remaining until market close (23:00 SAST)
    using local time in Africa/Johannesburg.
    """
    try:
        tz = ZoneInfo("Africa/Johannesburg")
        current_time = datetime.now(tz)
        # Define market close time (23:00) in the same time zone
        market_close_today = current_time.replace(
            hour=23, minute=0, second=0, microsecond=0
        )

        # If current time is already past 23:00, return 0
        if current_time > market_close_today:
            return "00:00:00"
        remaining = market_close_today - current_time
        
        # Convert to H:M:S
        total_seconds = int(remaining.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    except Exception as e:
        print(f"Error: {e}")
        return None


def log_update(data, close_timer, prediction, pred_accuracy):
    price = data["price"]
    open = data["open_price"]
    day_high = data["day_high"]
    day_low = data["day_low"]
    unit_diff, diff_direction = get_unit_diff(prediction, price)
    
    print("_____________________________________________________________________")
    print(f"Current Price:              {price}")
    print(f"Open Price:                 {open}")
    print(f"Daily High:                 {day_high}")
    print(f"Daily Low:                  {day_low}")
    print(f"Predicted Closing Price:    {round(prediction, 5)}")
    print(f"Predicted price is:         {round(unit_diff, 5)} units {diff_direction} than current price.")
    print(f"Prediction Confidence:      {pred_accuracy}%")
    print(f"Time to Market Close:       {close_timer}")
    print("_____________________________________________________________________")
    

def set_ticker(arg):
    if arg.upper() == "EURUSD" or arg.upper() == "EURUSD=X":
        return "EURUSD=X"
    else:
        print("Ticker not currently supported. Try EURUSD")
        
        
def get_unit_diff(prediction, price):
    diff = prediction - price
    if diff < 0:
        dir = "lower"
    else:
        dir = "higher"
    
    return abs(diff), dir


if __name__ == "__main__":
    main()