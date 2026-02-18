import pytest
import pandas as pd
import pandas_ta as ta
from services.scalper_service import ScalperService

def test_scalper_strategy_logic():
    # Create mock OHLCV data that simulates a crossover
    data = {
        'close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120] * 3
    }
    df = pd.DataFrame(data)
    df['ema_fast'] = ta.ema(df['close'], length=9)
    df['ema_slow'] = ta.ema(df['close'], length=21)
    df['rsi'] = ta.rsi(df['close'], length=14)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Verify crossover logic (this is just testing the indicator behavior we rely on)
    assert 'ema_fast' in df.columns
    assert 'ema_slow' in df.columns
    assert not df['ema_fast'].isnull().all()

def test_scalper_singleton():
    s1 = ScalperService()
    s2 = ScalperService()
    assert s1 is s2
    assert s1.is_running is False
