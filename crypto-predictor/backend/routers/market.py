import pandas as pd
from fastapi import APIRouter, HTTPException, Query
try:
    from ..services.coingecko import CoinGeckoService
    from ..services.indicators import IndicatorService
    from ..models.schemas import MarketOHLCVResponse, MarketOverviewResponse, OHLCVData
except ImportError:
    from services.coingecko import CoinGeckoService
    from services.indicators import IndicatorService
    from models.schemas import MarketOHLCVResponse, MarketOverviewResponse, OHLCVData
from typing import List

router = APIRouter(prefix="/market", tags=["market"])

@router.get("/ohlcv", response_model=MarketOHLCVResponse)
async def get_ohlcv(
    coin_id: str = Query(..., description="Coin ID (e.g., bitcoin)"),
    days: int = Query(30, description="Number of days (7|14|30|90)"),
    vs_currency: str = Query("usd", description="Currency (e.g., usd)")
):
    try:
        df = await CoinGeckoService.get_ohlcv(coin_id, days, vs_currency)
        # Compute indicators for the chart
        df = IndicatorService.compute_all(df)

        prices = []
        for _, row in df.iterrows():
            prices.append(OHLCVData(
                time=int(row['time']),
                open=float(row['open']),
                high=float(row['high']),
                low=float(row['low']),
                close=float(row['close']),
                volume=float(row['volume']),
                rsi=float(row['RSI']) if 'RSI' in row and not pd.isna(row['RSI']) else None,
                macd=float(row['MACD_12_26_9']) if 'MACD_12_26_9' in row and not pd.isna(row['MACD_12_26_9']) else None,
                macd_signal=float(row['MACDs_12_26_9']) if 'MACDs_12_26_9' in row and not pd.isna(row['MACDs_12_26_9']) else None,
                macd_hist=float(row['MACDh_12_26_9']) if 'MACDh_12_26_9' in row and not pd.isna(row['MACDh_12_26_9']) else None,
                bb_upper=float(row['BBU_20_2.0']) if 'BBU_20_2.0' in row and not pd.isna(row['BBU_20_2.0']) else None,
                bb_lower=float(row['BBL_20_2.0']) if 'BBL_20_2.0' in row and not pd.isna(row['BBL_20_2.0']) else None,
                bb_middle=float(row['BBM_20_2.0']) if 'BBM_20_2.0' in row and not pd.isna(row['BBM_20_2.0']) else None
            ))
        return MarketOHLCVResponse(symbol=coin_id.upper(), prices=prices)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/overview", response_model=MarketOverviewResponse)
async def get_overview(
    coin_id: str = Query(..., description="Coin ID (e.g., bitcoin)")
):
    try:
        data = await CoinGeckoService.get_market_overview(coin_id)
        return MarketOverviewResponse(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
