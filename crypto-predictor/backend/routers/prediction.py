from fastapi import APIRouter, HTTPException, Query
try:
    from ..services.coingecko import CoinGeckoService
    from ..services.prediction_engine import PredictionEngine
    from ..models.schemas import PredictionResponse
except ImportError:
    from services.coingecko import CoinGeckoService
    from services.prediction_engine import PredictionEngine
    from models.schemas import PredictionResponse

router = APIRouter(prefix="/prediction", tags=["prediction"])

@router.get("/signals", response_model=PredictionResponse)
async def get_signals(
    coin_id: str = Query(..., description="Coin ID (e.g., bitcoin)"),
    timeframe: str = Query("1d", description="Timeframe (1d|4h|1h)")
):
    try:
        # We use 'days' to get enough data for indicators
        # For 1d prediction, 90 days of history is good
        days = 90
        df = await CoinGeckoService.get_ohlcv(coin_id, days)
        prediction = PredictionEngine.calculate_signals(df)
        return PredictionResponse(**prediction)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
