from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class OHLCVData(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_hist: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_lower: Optional[float] = None
    bb_middle: Optional[float] = None

class MarketOHLCVResponse(BaseModel):
    symbol: str
    prices: List[OHLCVData]

class MarketOverviewResponse(BaseModel):
    name: str
    symbol: str
    current_price: float
    market_cap: float
    volume_24h: float
    price_change_24h: float
    price_change_7d: float
    ath: float
    atl: float
    circulating_supply: float

class SignalDetail(BaseModel):
    indicator: str
    value: float
    signal: str
    direction: str  # "bull" | "bear" | "neutral"
    weight: int

class PriceRange(BaseModel):
    low: float
    mid: float
    high: float

class PredictionResponse(BaseModel):
    overall_signal: str # "STRONG BUY" | "BUY" | "NEUTRAL" | "SELL" | "STRONG SELL"
    confidence: float
    predicted_direction: str # "UP" | "DOWN" | "SIDEWAYS"
    predicted_price_range: PriceRange
    horizon: str
    signals: List[SignalDetail]
    summary: str

class ExchangeConfig(BaseModel):
    exchange_id: str
    api_key: str
    secret: str
    passphrase: Optional[str] = None
    testnet: bool = True

class TradeSignal(BaseModel):
    timestamp: int
    symbol: str
    side: str # "buy" | "sell"
    price: float
    reason: str

class ScalperStatus(BaseModel):
    is_running: bool
    exchange_id: Optional[str] = None
    symbol: Optional[str] = None
    balance: Optional[float] = None
    recent_trades: List[TradeSignal] = []
