import pytest
import pandas as pd
import numpy as np
from services.prediction_engine import PredictionEngine

def test_prediction_logic():
    # Mock data for a Strong Buy signal
    # Low RSI, Bullish MACD, etc.
    data = {
        'time': range(100),
        'open': [100] * 100,
        'high': [110] * 100,
        'low': [90] * 100,
        'close': [100] * 100,
        'volume': [1000] * 100
    }
    # Modify last few rows to simulate a strong uptrend
    df = pd.DataFrame(data)
    df.loc[99, 'close'] = 120
    df.loc[99, 'volume'] = 2000

    result = PredictionEngine.calculate_signals(df)

    assert "overall_signal" in result
    assert "confidence" in result
    assert "signals" in result
    assert len(result["signals"]) > 0

def test_empty_df():
    with pytest.raises(ValueError):
        PredictionEngine.calculate_signals(pd.DataFrame())

def test_indicator_values():
    data = {
        'time': range(100),
        'open': np.linspace(100, 200, 100),
        'high': np.linspace(110, 210, 100),
        'low': np.linspace(90, 190, 100),
        'close': np.linspace(100, 200, 100),
        'volume': [1000] * 100
    }
    df = pd.DataFrame(data)
    result = PredictionEngine.calculate_signals(df)

    # Check if confidence is within range
    assert 50 <= result["confidence"] <= 100

    # Check if price range is valid
    assert result["predicted_price_range"]["low"] < result["predicted_price_range"]["high"]
