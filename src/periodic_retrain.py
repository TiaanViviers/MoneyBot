from fetch_hist_data import get_hist_data
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import os
import joblib


def retrain():
    """
Retrains the Random Forest model on the updated dataset.

This function updates the training dataset with the latest available data, scales the dataset, 
and retrains the Random Forest model using the scaled data. The retrained model and scaler are saved 
for deployment.

Steps:
1. Fetches the latest historical data and appends it to the existing dataset.
2. Loads the updated dataset from a specified CSV file.
3. Scales the dataset and saves the scaler for use in predictions.
4. Retrains the Random Forest model using the scaled data and saves the updated model.

Exceptions:
    Raises exceptions if any step of the retraining process fails, such as file I/O errors 
    or model training errors.
"""
    #update training set with latest data
    print("Updating training data...")
    get_hist_data("eur_usd_data", "EURUSD")
    
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
    """
Scales the dataset and saves the scaler for deployment.

This function standardizes the features in the dataset.
It saves the scaler for use in predictions during deployment. The target variable 
is included in scaling to maintain consistency with the training pipeline.

Args:
    data (pd.DataFrame): The input dataset to scale. Each column is treated as a feature.

Returns:
    pd.DataFrame: A DataFrame containing the scaled features, with the same structure as the input data.

"""
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