from fetch_hist_data import get_hist_data
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import os
import joblib


def retrain():
    #update training set with latest data
    print("Updating training data...")
    get_hist_data("eur_usd_data.csv", "EURUSD")
    
    #load the new csv file
    data = pd.read_csv("../data/raw/eur_usd_data.csv", parse_dates=["date"], index_col="date")
    print(f"Loaded data from {data.index.min()} to {data.index.max()}.")
    
    #scale the dataset and save scaler
    scaled_train_df = scale_df(data)
    print("Data scaled and scaler saved.")
    
    #retrain model and save model
    fit_model(scaled_train_df)
    print(f"Model retrained on all available data from {data.index.min().date()} to {data.index.max().date()}.")
    
    
    
def scale_df(data):
    scaler = StandardScaler()
    #scale training data
    scaled_train = scaler.fit_transform(data)
    scaled_train = pd.DataFrame(scaled_train, columns=data.columns, index=data.index)
    #save scalar for deployment
    scaler_directory = "../models/EURUSD_daily/"
    scaler_filename = "eurusd_scaler"
    scaler_path = os.path.join(scaler_directory, scaler_filename)
    joblib.dump(scaler, scaler_path)
    
    return scaled_train

def fit_model(data, save_path="../models/EURUSD_daily/rf_model_full_138.joblib"):
    """
    Retrains a RandomForestRegressor model on the provided data and saves the model.

    Args:
        data (pd.DataFrame): Scaled training data, with features and target.
        save_path (str): Path to save the retrained model.
    """
    try:
        print("Starting model retraining...")

        # Define features and target
        target_column = "Close"
        X = data.drop(columns=[target_column])
        y = data[target_column]

        # Define Random Forest hyperparameters
        rf_params = {
            'bootstrap': True,
            'ccp_alpha': 0.0,
            'criterion': 'squared_error',
            'max_depth': 10,
            'max_features': None,
            'max_leaf_nodes': None,
            'max_samples': None,
            'min_impurity_decrease': 0.0,
            'min_samples_leaf': 1,
            'min_samples_split': 2,
            'min_weight_fraction_leaf': 0.0,
            'monotonic_cst': None,
            'n_estimators': 200,
            'n_jobs': None,
            'oob_score': False,
            'random_state': 42,
            'verbose': 0,
            'warm_start': False
        }

        # Initialize and fit the Random Forest model
        rf_model = RandomForestRegressor(**rf_params)
        rf_model.fit(X, y)
        print("Model training completed successfully.")

        # Save the retrained model
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(rf_model, save_path)
        print(f"Model saved at: {save_path}")

    except Exception as e:
        print(f"Error during model retraining: {e}")
        raise