from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from .routers import market, prediction, trading
except ImportError:
    from routers import market, prediction, trading

app = FastAPI(title="Crypto Price Prediction API")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market.router, prefix="/api")
app.include_router(prediction.router, prefix="/api")
app.include_router(trading.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Crypto Price Prediction API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
