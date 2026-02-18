# Crypto Price Prediction Terminal

A professional-grade full-stack cryptocurrency price prediction web application that uses real market data, technical analysis indicators, and a weighted scoring engine to forecast short-term price direction.

## 🚀 Features

- **Real-time Market Data**: Integrated with CoinGecko API for live price and OHLCV data.
- **Advanced Technical Analysis**: Computes 10+ indicators including RSI, MACD, Bollinger Bands, SMA/EMA Crosses, Stochastic, ATR, etc.
- **Proprietary Prediction Engine**: A weighted scoring system that aggregates signals into a single actionable forecast.
- **Medium Frequency Scalper**: Background trading service with exchange connectivity (CCXT) supporting live and testnet environments.
- **Terminal UI**: A sleek, dark-themed dashboard inspired by professional trading terminals (Bloomberg, Reuters).
- **Responsive Charts**: Interactive price, RSI, and MACD panels using Recharts.

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Tailwind CSS, Recharts, TanStack Query, Zustand.
- **Backend**: FastAPI (Python 3.12), Pandas-TA, Scikit-learn, CCXT.
- **Containerization**: Docker & Docker Compose.

## 🏁 Getting Started

To access the terminal, follow these steps:

### Prerequisites

- Docker and Docker Compose
- Node.js & npm (for local development)
- Python 3.12 (for local development)

### Running with Docker

1. Navigate to the project directory:
   ```bash
   cd crypto-predictor
   ```
2. Start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. **Access the Web App**: Open your browser and go to **[http://localhost:3000](http://localhost:3000)**.

## 📖 Usage Guide

### 1. Market Dashboard
- **Coin Selection**: Use the dropdown in the header to switch between supported cryptocurrencies (BTC, ETH, SOL, etc.).
- **Timeframe Control**: Switch between 1D, 7D, 30D, and 90D views to analyze different historical horizons.
- **Price Chart**: An interactive candlestick chart shows price action and volume. Hover over candles to see specific OHLCV data.
- **Indicator Panels**: Monitor real-time RSI and MACD trends in the panels below the main chart.

### 2. Prediction Terminal
- **System Forecast**: The top-right panel displays the current algorithmic bias (e.g., STRONG BUY, NEUTRAL).
- **Confidence Level**: Shows the strength of the current signal based on indicator alignment.
- **Target Range**: Provides a predicted high/low range for the next 24 hours based on ATR (Average True Range).
- **Signal Cards**: Detailed breakdown of every technical indicator being tracked and its current directional bias (Bullish/Bearish).

### 3. Automated Scalper
- **Setup**: Click the "SCALPER" tab in the right sidebar.
- **Configuration**:
    - Select your **Exchange** (e.g., Binance, Bybit).
    - Enter your **API Key** and **Secret**.
    - Toggle **Testnet** (Highly Recommended) to trade with virtual funds.
- **Execution**: Click **Start Scalper**. The bot will monitor the 1-minute timeframe for EMA crossovers and RSI confirmations.
- **Logs**: Monitor the real-time execution log at the bottom of the scalper panel to track orders and signals.

### Local Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧠 How the Prediction Engine Works

The system uses a **weighted scoring engine** to evaluate multiple technical indicators:

| Indicator | Weight | Logic |
|-----------|--------|-------|
| RSI | 20 | Identifies overbought/oversold conditions |
| MACD | 25 | Trend momentum and crossovers |
| Bollinger Bands | 15 | Volatility and price extremes |
| SMA Cross | 20 | Long-term trend confirmation |
| ... | ... | ... |

Each indicator contributes a score based on its current signal (Bullish: +Weight, Bearish: -Weight, Neutral: 0). The final score is normalized to a range of -100 to +100 and mapped to signals:
- **+60 to +100**: STRONG BUY
- **+20 to +59**: BUY
- **-19 to +19**: NEUTRAL
- **-59 to -20**: SELL
- **-100 to -60**: STRONG SELL

## ⚡ Medium Frequency Scalper

The integrated Scalper feature allows users to:
1. Connect to various exchanges (Binance, Bybit, Kraken, etc.) via API keys.
2. Toggle between **Live** and **Testnet** environments.
3. Run an automated **EMA Cross + RSI** strategy in the background.
4. Monitor execution logs in real-time through the terminal dashboard.

*Note: For security, API keys are kept in-memory for the duration of the session and are not persisted to a database.*

## ⚠️ Disclaimer

**This tool is for educational and informational purposes only. Crypto markets are highly volatile. Past indicator patterns do not guarantee future results. Never invest based solely on algorithmic signals.**
