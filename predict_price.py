import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import datetime

def predict_stock_price(ticker_symbol):
    # 1. Download historical data (last 1 year)
    print(f"Fetching data for {ticker_symbol}...")
    data = yf.download(ticker_symbol, period="1y", interval="1d")

    if data.empty:
        print("Error: No data found for the ticker.")
        return

    # Flatten MultiIndex if necessary (common in recent yfinance versions)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # 2. Data Preprocessing
    # Use 'Close' price for prediction
    df = data[['Close']].copy()

    # Create features: Moving Averages
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA20'] = df['Close'].rolling(window=20).mean()

    # Drop rows with NaN values (from rolling windows)
    df.dropna(inplace=True)

    # Target: Next day's closing price
    df['Target'] = df['Close'].shift(-1)

    # Last row has NaN for Target, save it for prediction later
    latest_data = df.iloc[-1:].drop(columns=['Target'])
    df.dropna(inplace=True)

    # 3. Model Training
    X = df[['Close', 'MA5', 'MA20']]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    # 4. Evaluation
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    # 5. Prediction for the next day
    next_day_prediction = model.predict(latest_data)

    # Extract scalar values safely
    current_price = latest_data['Close'].iloc[0]
    predicted_val = next_day_prediction[0]

    print("\n--- Results ---")
    print(f"Ticker: {ticker_symbol}")
    print(f"Current Price (Latest Close): ${float(current_price):.2f}")
    print(f"Predicted Price for Next Trading Day: ${float(predicted_val):.2f}")
    print(f"Model RMSE: {float(rmse):.4f}")
    print("----------------")

    return next_day_prediction[0]

if __name__ == "__main__":
    predict_stock_price("AAPL")
