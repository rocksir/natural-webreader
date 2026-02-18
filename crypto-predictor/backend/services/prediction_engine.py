import pandas as pd
import numpy as np
from typing import Dict, List, Any
try:
    from .indicators import IndicatorService
except ImportError:
    from services.indicators import IndicatorService

INDICATOR_WEIGHTS = {
    "RSI": 20,
    "MACD": 25,
    "Bollinger Bands": 15,
    "SMA Cross": 20,
    "EMA Cross": 10,
    "Stochastic": 10,
    "Volume Trend": 15,
    "Williams %R": 10,
    "CCI": 10,
}

class PredictionEngine:
    @staticmethod
    def calculate_signals(df: pd.DataFrame) -> Dict[str, Any]:
        if df.empty:
            raise ValueError("Empty DataFrame provided to prediction engine")

        df = IndicatorService.compute_all(df)
        # Ensure all columns exist to avoid KeyError, fill NaN with 0 for safety
        df = df.fillna(0)

        last_row = df.iloc[-1]
        prev_row = df.iloc[-2] if len(df) > 1 else last_row

        signals = []
        total_score = 0

        # 1. RSI (14)
        # <30 = Oversold (Bullish), >70 = Overbought (Bearish), 30–50 = Mild Bear, 50–70 = Mild Bull
        rsi = last_row['RSI']
        rsi_signal = "NEUTRAL"
        rsi_dir = "neutral"
        rsi_score = 0
        if rsi < 30:
            rsi_signal = "Oversold"
            rsi_dir = "bull"
            rsi_score = 1
        elif rsi > 70:
            rsi_signal = "Overbought"
            rsi_dir = "bear"
            rsi_score = -1
        elif 30 <= rsi < 50:
            rsi_signal = "Mild Bearish"
            rsi_dir = "bear"
            rsi_score = -0.5
        elif 50 <= rsi <= 70:
            rsi_signal = "Mild Bullish"
            rsi_dir = "bull"
            rsi_score = 0.5

        signals.append({
            "indicator": "RSI (14)",
            "value": round(float(rsi), 2) if not pd.isna(rsi) else 0,
            "signal": rsi_signal,
            "direction": rsi_dir,
            "weight": INDICATOR_WEIGHTS["RSI"]
        })
        total_score += rsi_score * INDICATOR_WEIGHTS["RSI"]

        # 2. MACD (12, 26, 9)
        # MACD > Signal + positive histogram = Bull cross; opposite = Bear cross
        macd_val = last_row.get('MACD_12_26_9', 0)
        macd_sig = last_row.get('MACDs_12_26_9', 0)
        macd_hist = last_row.get('MACDh_12_26_9', 0)

        m_signal = "NEUTRAL"
        m_dir = "neutral"
        m_score = 0
        if macd_val > macd_sig and macd_hist > 0:
            m_signal = "Bullish Cross"
            m_dir = "bull"
            m_score = 1
        elif macd_val < macd_sig and macd_hist < 0:
            m_signal = "Bearish Cross"
            m_dir = "bear"
            m_score = -1

        signals.append({
            "indicator": "MACD (12,26,9)",
            "value": round(float(macd_hist), 2) if not pd.isna(macd_hist) else 0,
            "signal": m_signal,
            "direction": m_dir,
            "weight": INDICATOR_WEIGHTS["MACD"]
        })
        total_score += m_score * INDICATOR_WEIGHTS["MACD"]

        # 3. Bollinger Bands (20, 2)
        # Price < lower band = Oversold/Bull; Price > upper band = Overbought/Bear
        close = last_row['close']
        bb_lower = last_row.get('BBL_20_2.0', 0)
        bb_upper = last_row.get('BBU_20_2.0', 0)

        bb_signal = "NEUTRAL"
        bb_dir = "neutral"
        bb_score = 0
        if close < bb_lower:
            bb_signal = "Below Lower Band"
            bb_dir = "bull"
            bb_score = 1
        elif close > bb_upper:
            bb_signal = "Above Upper Band"
            bb_dir = "bear"
            bb_score = -1

        signals.append({
            "indicator": "Bollinger Bands",
            "value": round(float(close), 2),
            "signal": bb_signal,
            "direction": bb_dir,
            "weight": INDICATOR_WEIGHTS["Bollinger Bands"]
        })
        total_score += bb_score * INDICATOR_WEIGHTS["Bollinger Bands"]

        # 4. SMA Cross (20/50)
        # SMA20 > SMA50 = Golden cross (Bull); SMA20 < SMA50 = Death cross (Bear)
        sma20 = last_row.get('SMA_20', 0)
        sma50 = last_row.get('SMA_50', 0)

        sma_signal = "NEUTRAL"
        sma_dir = "neutral"
        sma_score = 0
        if sma20 > sma50:
            sma_signal = "Golden Cross"
            sma_dir = "bull"
            sma_score = 1
        elif sma20 < sma50:
            sma_signal = "Death Cross"
            sma_dir = "bear"
            sma_score = -1

        signals.append({
            "indicator": "SMA Cross (20/50)",
            "value": round(float(sma20 - sma50), 2) if not pd.isna(sma20-sma50) else 0,
            "signal": sma_signal,
            "direction": sma_dir,
            "weight": INDICATOR_WEIGHTS["SMA Cross"]
        })
        total_score += sma_score * INDICATOR_WEIGHTS["SMA Cross"]

        # 5. EMA Cross (9/21)
        ema9 = last_row.get('EMA_9', 0)
        ema21 = last_row.get('EMA_21', 0)

        ema_signal = "NEUTRAL"
        ema_dir = "neutral"
        ema_score = 0
        if ema9 > ema21:
            ema_signal = "Bullish Trend"
            ema_dir = "bull"
            ema_score = 1
        elif ema9 < ema21:
            ema_signal = "Bearish Trend"
            ema_dir = "bear"
            ema_score = -1

        signals.append({
            "indicator": "EMA Cross (9/21)",
            "value": round(float(ema9 - ema21), 2) if not pd.isna(ema9-ema21) else 0,
            "signal": ema_signal,
            "direction": ema_dir,
            "weight": INDICATOR_WEIGHTS["EMA Cross"]
        })
        total_score += ema_score * INDICATOR_WEIGHTS["EMA Cross"]

        # 6. Stochastic (14,3,3)
        stoch_k = last_row.get('STOCHk_14_3_3', 50)

        stoch_signal = "NEUTRAL"
        stoch_dir = "neutral"
        stoch_score = 0
        if stoch_k < 20:
            stoch_signal = "Oversold"
            stoch_dir = "bull"
            stoch_score = 1
        elif stoch_k > 80:
            stoch_signal = "Overbought"
            stoch_dir = "bear"
            stoch_score = -1

        signals.append({
            "indicator": "Stochastic",
            "value": round(float(stoch_k), 2) if not pd.isna(stoch_k) else 0,
            "signal": stoch_signal,
            "direction": stoch_dir,
            "weight": INDICATOR_WEIGHTS["Stochastic"]
        })
        total_score += stoch_score * INDICATOR_WEIGHTS["Stochastic"]

        # 7. Volume Trend
        # Rising volume + rising price = confirmed Bull; Rising volume + falling price = confirmed Bear
        vol_change = last_row.get('vol_change', 0)
        price_change = last_row.get('price_change', 0)

        vol_signal = "NEUTRAL"
        vol_dir = "neutral"
        vol_score = 0
        if vol_change > 0 and price_change > 0:
            vol_signal = "Bullish Volume"
            vol_dir = "bull"
            vol_score = 1
        elif vol_change > 0 and price_change < 0:
            vol_signal = "Bearish Volume"
            vol_dir = "bear"
            vol_score = -1

        signals.append({
            "indicator": "Volume Trend",
            "value": round(float(vol_change), 2) if not pd.isna(vol_change) else 0,
            "signal": vol_signal,
            "direction": vol_dir,
            "weight": INDICATOR_WEIGHTS["Volume Trend"]
        })
        total_score += vol_score * INDICATOR_WEIGHTS["Volume Trend"]

        # 8. Williams %R (14)
        willr = last_row.get('WILLR', -50)
        willr_signal = "NEUTRAL"
        willr_dir = "neutral"
        willr_score = 0
        if willr < -80:
            willr_signal = "Oversold"
            willr_dir = "bull"
            willr_score = 1
        elif willr > -20:
            willr_signal = "Overbought"
            willr_dir = "bear"
            willr_score = -1

        signals.append({
            "indicator": "Williams %R",
            "value": round(float(willr), 2) if not pd.isna(willr) else 0,
            "signal": willr_signal,
            "direction": willr_dir,
            "weight": INDICATOR_WEIGHTS["Williams %R"]
        })
        total_score += willr_score * INDICATOR_WEIGHTS["Williams %R"]

        # 9. CCI (20)
        cci = last_row.get('CCI', 0)
        cci_signal = "NEUTRAL"
        cci_dir = "neutral"
        cci_score = 0
        if cci > 100:
            cci_signal = "Bullish Momentum"
            cci_dir = "bull"
            cci_score = 1
        elif cci < -100:
            cci_signal = "Bearish Momentum"
            cci_dir = "bear"
            cci_score = -1

        signals.append({
            "indicator": "CCI (20)",
            "value": round(float(cci), 2) if not pd.isna(cci) else 0,
            "signal": cci_signal,
            "direction": cci_dir,
            "weight": INDICATOR_WEIGHTS["CCI"]
        })
        total_score += cci_score * INDICATOR_WEIGHTS["CCI"]

        # Final Score Normalization
        max_possible_score = sum(INDICATOR_WEIGHTS.values())
        normalized_score = (total_score / max_possible_score) * 100

        overall_signal = "NEUTRAL"
        if normalized_score >= 60: overall_signal = "STRONG BUY"
        elif normalized_score >= 20: overall_signal = "BUY"
        elif normalized_score <= -60: overall_signal = "STRONG SELL"
        elif normalized_score <= -20: overall_signal = "SELL"

        predicted_direction = "SIDEWAYS"
        if normalized_score > 20: predicted_direction = "UP"
        elif normalized_score < -20: predicted_direction = "DOWN"

        confidence = abs(normalized_score)
        # Map 0-100 to 50-99
        confidence = 50 + (confidence * 0.49)

        atr = last_row.get('ATR', close * 0.05)
        # Predicted price range = current_price ± (ATR * multiplier based on confidence)
        multiplier = 1 + (confidence / 100)
        predicted_price_range = {
            "low": round(close - (atr * multiplier), 2),
            "mid": round(close + (normalized_score/100 * atr * multiplier), 2),
            "high": round(close + (atr * multiplier), 2)
        }

        summary = f"The overall market sentiment for this coin is {overall_signal} with a confidence of {round(confidence, 1)}%. "
        if predicted_direction == "UP":
            summary += "Technical indicators suggest an upward momentum in the short term."
        elif predicted_direction == "DOWN":
            summary += "Indicators point towards a bearish trend, suggesting potential price drops."
        else:
            summary += "The market is currently showing mixed signals, suggesting sideways movement."

        return {
            "overall_signal": overall_signal,
            "confidence": round(confidence, 2),
            "predicted_direction": predicted_direction,
            "predicted_price_range": predicted_price_range,
            "horizon": "24h",
            "signals": signals,
            "summary": summary
        }
