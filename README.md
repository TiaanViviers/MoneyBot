# MoneyBot, a EUR/USD Price Prediction and Deployment System

## Overview
This project provides a robust system for predicting the EUR/USD exchange rate using machine learning. We trained multiple models (Random Forest, XGBoost, and LSTM), evaluated their performance, and integrated the best‐performing model into a real‐time prediction pipeline.

**Key Capabilities:**
- Fetch live exchange rate data (via APIs or web scraping).
- Predict closing prices using intraday data.
- Track daily highs and lows for improved accuracy.
- Periodically retrain models with updated historical data.

---

## Table of Contents
1. [Features](#features)  
2. [Installation](#installation)  
3. [Data Pipeline](#data-pipeline)  
4. [Model Development](#model-development)  
   - [Data Preparation](#data-preparation)  
   - [Model Training](#model-training)  
   - [Model Comparison](#model-comparison)  
5. [Deployment System](#deployment-system)  
   - [Periodic Retraining](#periodic-retraining)  
6. [Results](#results)  
7. [Future Enhancements](#future-enhancements)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Features
- **Historical + Live Data Ingestion:** Retrieve exchange rate data from APIs (Alpha Vantage) or Yahoo Finance (via web scraping).  
- **Predictive Model Ensemble:** Compare Random Forest, XGBoost, and LSTM to identify the top‐performing model.  
- **Real‐Time Price Insights:** Monitor intraday data (current price, daily high, daily low) and provide on‐demand predictions.  
- **Periodic Retraining:** Continuously update the model with new data for improved accuracy.  
- **Confidence & Metrics:** Offer confidence estimates and standard evaluation metrics (MSE, MAE, R²).

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/TiaanViviers/MoneyBot.git
cd MoneyBot
```

### 2. Install dependencies
Install dependancies from requirements.txt file

### 4. Set up Environment Variables
You will need a Alpha Vantage API key saved in a .env file in the `config` directory


## Data Pipeline
- **Fetch Historical Data:** Retrieve past rates from Alpha Vantage and store them in `../data/raw/eur_usd_data.csv`.
- **Fetch Live Data:** Query Alpha Vantage or scrape Yahoo Finance for real‐time quotes.
- **Scaling:** Apply `StandardScaler` to features (`Open`, `High`, `Low`, `Close`). The scaler is saved in `../models/EURUSD_daily/eurusd_scaler`.

---

## Model Development

### Data Preparation
- **Features:** `Open`, `High`, `Low`
- **Target:** `Close`
- **Scaling:** Used a `StandardScaler` for feature transformation.

### Model Training

1. **Random Forest**  
   - Hyperparameters: `max_depth=10`, `n_estimators=200`, etc.  
   - Implementation: `sklearn.ensemble.RandomForestRegressor`

2. **XGBoost**  
   - Hyperparameters: Learning rate, tree depth, etc.  
   - Implementation: `xgboost.XGBRegressor`

3. **LSTM**  
   - Hyperparameters: Layer count, units, dropout, etc.  
   - Implementation: `tensorflow.keras.Sequential`

### Model Comparison
Models were evaluated on:
- Mean Squared Error (MSE)  
- Mean Absolute Error (MAE)  
- R² Score  

A weighted scoring system (33.33% each) identified **Random Forest** as the best model with a weighted score of **0.95**.

---

## Deployment System
The deployment includes:
- **`live_price_api.py`** – Fetches live data from Alpha Vantage.  
- **`trade_bot.py`** – Applies scaling and loads the trained model to predict.  
- **`yahoo_scrape.py`** – Scrapes Yahoo Finance for real‐time data.

### Periodic Retraining
A scheduled process:
1. Fetches updated historical data.  
2. Retrains the best‐performing model with new data.  
3. Saves the updated model and scaler for live prediction.

---

## Results
| model_name | mse      | mae      | r2       | normalized_mse | normalized_mae | normalized_r2 | weighted_score | rank |
|------------|----------|----------|----------|----------------|----------------|---------------|---------------|------|
| rf_138     | 0.000545 | 0.008133 | 0.983302 | 1.000000       | 1.000000       | 1.000000      | 0.999900      | 1.0  |
| rf_219     | 0.000553 | 0.008546 | 0.983058 | 0.999772       | 0.997574       | 0.999772      | 0.998939      | 2.0  |
| rf_300     | 0.000553 | 0.008546 | 0.983058 | 0.999772       | 0.997574       | 0.999772      | 0.998939      | 3.0  |
| xgb_283    | 0.001724 | 0.026180 | 0.947195 | 0.966302       | 0.894058       | 0.966302      | 0.942127      | 4.0  |
| xgb_277    | 0.001751 | 0.026441 | 0.946384 | 0.965545       | 0.892527       | 0.965545      | 0.941112      | 5.0  |
| xgb_281    | 0.001723 | 0.026744 | 0.947237 | 0.966342       | 0.890749       | 0.966342      | 0.941050      | 6.0  |
| lstm_2     | 0.003609 | 0.042512 | 0.889476 | 0.912435       | 0.798190       | 0.912435      | 0.874266      | 7.0  |
| lstm_1     | 0.020458 | 0.129884 | 0.373418 | 0.430813       | 0.285296       | 0.430813      | 0.382269      | 8.0  |
| lstm_3     | 0.035530 | 0.178485 | -0.088200| 0.000000       | 0.000000       | 0.000000      | 0.000000      | 9.0  |

**Observations:**
- **Random Forest** demonstrated the best overall performance.  
- **XGBoost** was a close second.  
- **LSTM** underperformed, likely due to complex hyperparameter tuning.

---

## Future Enhancements 
- **Chat/Telegram Integration:** Send alerts or daily summaries for significant market moves.  
- **Support Additional Assets:** Extend coverage to other forex pairs, equities, and cryptocurrencies.  
- **Automated Deployment:** Use Docker or similar tooling for seamless production.

---

## Contributing
1. Fork this repository.  
2. Create a new feature branch.  
3. Commit your changes.  
4. Submit a pull request.

---

## License
This project is licensed under the **MIT License**.

