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
    

    def get_pred_accuracy(self):
        """
        Placeholder for getting prediction accuracy.

        Returns:
            None
        """
        pass
    
    
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