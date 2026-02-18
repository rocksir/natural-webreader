import pandas as pd
import pandas_ta as ta

class IndicatorService:
    @staticmethod
    def compute_all(df: pd.DataFrame) -> pd.DataFrame:
        """
        Computes all required TA indicators on the provided OHLCV DataFrame.
        """
        # Ensure data is sorted by time
        df = df.sort_values('time').reset_index(drop=True)

        # RSI (14)
        df['RSI'] = ta.rsi(df['close'], length=14)

        # MACD (12, 26, 9)
        macd = ta.macd(df['close'], fast=12, slow=26, signal=9)
        if macd is not None:
            df = pd.concat([df, macd], axis=1)

        # Bollinger Bands (20, 2)
        bb = ta.bbands(df['close'], length=20, std=2)
        if bb is not None:
            df = pd.concat([df, bb], axis=1)

        # SMA 20/50
        df['SMA_20'] = ta.sma(df['close'], length=20)
        df['SMA_50'] = ta.sma(df['close'], length=50)

        # EMA 9/21
        df['EMA_9'] = ta.ema(df['close'], length=9)
        df['EMA_21'] = ta.ema(df['close'], length=21)

        # Stochastic (14, 3, 3)
        stoch = ta.stoch(df['high'], df['low'], df['close'], k=14, d=3, smooth_k=3)
        if stoch is not None:
            df = pd.concat([df, stoch], axis=1)

        # ATR (14)
        df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)

        # Williams %R (14)
        df['WILLR'] = ta.willr(df['high'], df['low'], df['close'], length=14)

        # CCI (20)
        df['CCI'] = ta.cci(df['high'], df['low'], df['close'], length=20)

        # Volume Trend: Rising volume + rising price = confirmed Bull
        # We can calculate rolling average of volume and price change
        df['vol_change'] = df['volume'].pct_change()
        df['price_change'] = df['close'].pct_change()

        return df
