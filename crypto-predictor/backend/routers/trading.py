from fastapi import APIRouter, HTTPException, BackgroundTasks
try:
    from ..models.schemas import ExchangeConfig, ScalperStatus
    from ..services.exchange_service import ExchangeService
    from ..services.scalper_service import ScalperService
except ImportError:
    from models.schemas import ExchangeConfig, ScalperStatus
    from services.exchange_service import ExchangeService
    from services.scalper_service import ScalperService
from typing import Dict, Any

router = APIRouter(prefix="/trading", tags=["trading"])
scalper_service = ScalperService()

@router.post("/start")
async def start_scalper(config: ExchangeConfig, symbol: str = "BTC/USDT"):
    try:
        exchange_service = ExchangeService(
            exchange_id=config.exchange_id,
            api_key=config.api_key,
            secret=config.secret,
            passphrase=config.passphrase,
            testnet=config.testnet
        )
        # Check connection
        await exchange_service.get_balance()

        scalper_service.start(exchange_service, symbol)
        return {"message": "Scalper started successfully", "status": scalper_service.get_status()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to start scalper: {str(e)}")

@router.post("/stop")
async def stop_scalper():
    scalper_service.stop()
    return {"message": "Scalper stopped successfully", "status": scalper_service.get_status()}

@router.get("/status")
async def get_scalper_status():
    return scalper_service.get_status()
