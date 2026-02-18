import ccxt.async_support as ccxt
from typing import Optional, Dict, Any

class ExchangeService:
    def __init__(self, exchange_id: str, api_key: str, secret: str, passphrase: Optional[str] = None, testnet: bool = True):
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': secret,
            'password': passphrase,
            'enableRateLimit': True,
        })
        if testnet:
            if hasattr(self.exchange, 'set_sandbox_mode'):
                self.exchange.set_sandbox_mode(True)
            else:
                # Some exchanges use urls['test']
                if 'test' in self.exchange.urls:
                    self.exchange.urls['api'] = self.exchange.urls['test']

    async def get_balance(self, currency: str = 'USDT') -> float:
        try:
            balance = await self.exchange.fetch_balance()
            return balance.get('total', {}).get(currency, 0.0)
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0.0

    async def create_market_order(self, symbol: str, side: str, amount: float):
        try:
            if side == 'buy':
                return await self.exchange.create_market_buy_order(symbol, amount)
            else:
                return await self.exchange.create_market_sell_order(symbol, amount)
        except Exception as e:
            print(f"Error creating order: {e}")
            return None

    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        return await self.exchange.fetch_ticker(symbol)

    async def close(self):
        await self.exchange.close()
