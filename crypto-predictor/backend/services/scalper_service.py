import asyncio
import time
import pandas as pd
import pandas_ta as ta
from typing import List, Dict, Optional, Any
try:
    from .exchange_service import ExchangeService
    from ..models.schemas import TradeSignal
except ImportError:
    from services.exchange_service import ExchangeService
    from models.schemas import TradeSignal

class ScalperService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScalperService, cls).__new__(cls)
            cls._instance.is_running = False
            cls._instance.task = None
            cls._instance.exchange_service = None
            cls._instance.symbol = None
            cls._instance.trades: List[TradeSignal] = []
            cls._instance.logs: List[str] = []
        return cls._instance

    def start(self, exchange_service: ExchangeService, symbol: str):
        if self.is_running:
            return
        self.is_running = True
        self.exchange_service = exchange_service
        self.symbol = symbol
        self.task = asyncio.create_task(self._run_loop())
        self._add_log(f"Scalper started for {symbol}")

    def stop(self):
        self.is_running = False
        if self.task:
            self.task.cancel()

        asyncio.create_task(self._cleanup())
        self._add_log("Scalper stopped")

    async def _cleanup(self):
        if self.exchange_service:
            await self.exchange_service.close()

    def _add_log(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
        if len(self.logs) > 100:
            self.logs.pop(0)

    async def _run_loop(self):
        while self.is_running:
            try:
                # 1. Fetch OHLCV (1m timeframe for scalping)
                ohlcv = await self.exchange_service.exchange.fetch_ohlcv(self.symbol, timeframe='1m', limit=50)
                df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])

                # 2. Compute Indicators
                df['ema_fast'] = ta.ema(df['close'], length=9)
                df['ema_slow'] = ta.ema(df['close'], length=21)
                df['rsi'] = ta.rsi(df['close'], length=14)

                last = df.iloc[-1]
                prev = df.iloc[-2]

                self._add_log(f"Price: {last['close']} | EMA Fast: {round(last['ema_fast'], 2)} | EMA Slow: {round(last['ema_slow'], 2)} | RSI: {round(last['rsi'], 2)}")

                # 3. Strategy: EMA Crossover + RSI Confirmation
                # Buy when Fast EMA crosses above Slow EMA and RSI > 50
                if prev['ema_fast'] <= prev['ema_slow'] and last['ema_fast'] > last['ema_slow'] and last['rsi'] > 50:
                    self._add_log(f"🚀 BULLISH SIGNAL detected at {last['close']}")
                    # In a real scenario, we'd place an order here
                    # await self.exchange_service.create_market_order(self.symbol, 'buy', 0.001)
                    self.trades.append(TradeSignal(
                        timestamp=int(time.time() * 1000),
                        symbol=self.symbol,
                        side="buy",
                        price=float(last['close']),
                        reason="EMA Gold Cross + RSI Bull"
                    ))

                # Sell when Fast EMA crosses below Slow EMA and RSI < 50
                elif prev['ema_fast'] >= prev['ema_slow'] and last['ema_fast'] < last['ema_slow'] and last['rsi'] < 50:
                    self._add_log(f"📉 BEARISH SIGNAL detected at {last['close']}")
                    # await self.exchange_service.create_market_order(self.symbol, 'sell', 0.001)
                    self.trades.append(TradeSignal(
                        timestamp=int(time.time() * 1000),
                        symbol=self.symbol,
                        side="sell",
                        price=float(last['close']),
                        reason="EMA Death Cross + RSI Bear"
                    ))

                await asyncio.sleep(60) # Wait for next candle

            except asyncio.CancelledError:
                break
            except Exception as e:
                self._add_log(f"Error in scalper loop: {e}")
                await asyncio.sleep(10)

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "symbol": self.symbol,
            "recent_trades": self.trades[-10:],
            "logs": self.logs[-20:]
        }
