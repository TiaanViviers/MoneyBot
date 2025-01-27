import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd


class TradeBot:
    """
    A class to deploy the trading bot.
    Provides methods to make predictions and retrieve prediction accuracy.
    """

    def __init__(self):
        """
        Initialize the TradingBot instance.

        Args:
            model_path (str): Path to the trained Random Forest model (.joblib file).
            scaler_path (str): Path to the trained StandardScaler (.joblib file).
        """
        self.model_path = "../models/EURUSD_daily/rf_model_full_138.joblib"
        self.scaler_path = "../models/EURUSD_daily/eurusd_scaler"
        self.model = self._load_model()
        self.scaler = self._load_scaler()
        

    def _load_model(self):
        """
        Load the Random Forest model from the specified file.

        Returns:
            model: The loaded Random Forest model.
        """
        try:
            model = joblib.load(self.model_path)
            return model
        except Exception as e:
            raise ValueError(f"Error loading model: {e}")
        

    def _load_scaler(self):
        """
        Load the trained StandardScaler from the specified file.

        Returns:
            StandardScaler: The loaded scaler.
        """
        try:
            scaler = joblib.load(self.scaler_path)
            return scaler
        except Exception as e:
            raise ValueError(f"Error loading scaler: {e}")


    def scale(self, data):
        """
        Extract and scale the features for prediction.

        Args:
            data (dict): Input data with fields 'price', 'day_high', 'day_low', and 'open_price'.

        Returns:
            np.array: Scaled features in the order ['Open', 'High', 'Low'].
        """
        try:
            # Extract features from the data dictionary
            features = pd.DataFrame([{
                "Open": data["open_price"],
                "High": data["day_high"],
                "Low": data["day_low"],
                "Close": 0
            }])

            # Scale the features
            scaled_features = self.scaler.transform(features)
            scaled_df = pd.DataFrame(scaled_features, columns=features.columns)
            return scaled_df[["Open", "High", "Low"]]
        
        except Exception as e:
            raise ValueError(f"Error during scaling: {e}")
    

    def inverse_scale(self, prediction):
        """
        Inverse scale the prediction to return it to the original metric.

        Args:
            prediction (np.array): The scaled prediction.

        Returns:
            float: The inverse scaled prediction.
        """
        # Create a dummy dataframe with the prediction to apply inverse scaling
        dummy_input = [[0, 0, 0, prediction[0]]]
        dummy_df = pd.DataFrame(dummy_input, columns=["Open", "High", "Low", "Close"])
        inverse_scaled = self.scaler.inverse_transform(dummy_df)
        return inverse_scaled[0, 3]
    

    def predict(self, data):
        """
        Make a prediction using the loaded Random Forest model.

        Args:
            data (dict): Input data with fields 'price', 'day_high', 'day_low', and 'open_price'.

        Returns:
            float: The predicted value (e.g., closing price).
        """
        if not self.model:
            raise ValueError("Model not loaded.")
        
        # Extract and scale features
        features = self.scale(data)
        # Make the prediction
        prediction = self.model.predict(features)
        # Inverse scale the prediction
        return self.inverse_scale(prediction)
    

    def pred_confidence(self, time_to_close):
        """
        Calculate how confident we are in the daily close prediction based on
        how much time is left until the daily candle closes.

        Args:
            time_to_close (str): Time remaining in HH:MM:SS format (e.g. "10:29:38").

        Returns:
            float: Confidence in percent (0.0 to 100.0).
        """
        h, m, s = time_to_close.split(":")
        hours = int(h)
        minutes = int(m)
        seconds = int(s)

        #Convert to total seconds
        remaining_secs = hours * 3600 + minutes * 60 + seconds
        daily_session_secs = 86400

        #Calculate confidence as a ratio of how much of the day has elapsed
        elapsed_ratio = 1.0 - (remaining_secs / daily_session_secs)
        confidence_percent = max(0.0, min(100.0, elapsed_ratio * 100))

        return round(confidence_percent, 2)
    
    
#Test client
if __name__ == "__main__":
    bot = TradeBot()
    
    data = {
        "price": 1.0493,
        "day_high": 1.0500,
        "day_low": 1.0480,
        "open_price": 1.0490
    }

    try:
        prediction = bot.predict(data)
        print(f"Predicted closing price: {prediction}")
    except Exception as e:
        print(f"Error during prediction: {e}")