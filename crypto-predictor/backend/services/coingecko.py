import httpx
import pandas as pd
from cachetools import TTLCache, cached
from typing import Dict, List, Any, Optional

BASE_URL = "https://api.coingecko.com/api/v3"

# Cache for 5 minutes
ohlcv_cache = TTLCache(maxsize=100, ttl=300)
overview_cache = TTLCache(maxsize=100, ttl=60)

class CoinGeckoService:
    @staticmethod
    async def get_ohlcv(coin_id: str, days: int = 30, vs_currency: str = "usd") -> pd.DataFrame:
        """
        Fetches OHLCV data from CoinGecko and returns a pandas DataFrame.
        CoinGecko 'ohlc' endpoint provides: [time, open, high, low, close]
        We need volume too, so we might need 'market_chart' and merge.
        Actually, CoinGecko OHLC endpoint doesn't include volume.
        'market_chart' includes prices and total_volumes.
        """
        cache_key = f"ohlcv_{coin_id}_{days}_{vs_currency}"
        if cache_key in ohlcv_cache:
            return ohlcv_cache[cache_key]

        async with httpx.AsyncClient() as client:
            # CoinGecko OHLC endpoint
            ohlc_url = f"{BASE_URL}/coins/{coin_id}/ohlc"
            params = {"vs_currency": vs_currency, "days": days}
            ohlc_resp = await client.get(ohlc_url, params=params)
            ohlc_resp.raise_for_status()
            ohlc_data = ohlc_resp.json()

            # CoinGecko market_chart for volume
            mc_url = f"{BASE_URL}/coins/{coin_id}/market_chart"
            mc_params = {"vs_currency": vs_currency, "days": days}
            mc_resp = await client.get(mc_url, params=mc_params)
            mc_resp.raise_for_status()
            mc_data = mc_resp.json()

            # mc_data['total_volumes'] is [[time, volume], ...]
            volumes_dict = {item[0]: item[1] for item in mc_data['total_volumes']}

            # Create DataFrame
            df = pd.DataFrame(ohlc_data, columns=['time', 'open', 'high', 'low', 'close'])

            # Map volumes. Since OHLC and market_chart might have different frequencies,
            # we try to match them or take the closest.
            # Usually OHLC for 1-2 days is 30m, 3-30 days is 4h, >30 days is 4d.
            # We'll just try to match timestamps or use a simple merge.
            df['volume'] = df['time'].map(volumes_dict).fillna(0)

            # If volume is 0, try to find the nearest volume
            if (df['volume'] == 0).any():
                v_df = pd.DataFrame(mc_data['total_volumes'], columns=['time', 'volume'])
                df = pd.merge_asof(df.sort_values('time'), v_df.sort_values('time'), on='time', direction='nearest', suffixes=('', '_new'))
                df['volume'] = df['volume_new']
                df.drop(columns=['volume_new'], inplace=True)

            ohlcv_cache[cache_key] = df
            return df

    @staticmethod
    async def get_market_overview(coin_id: str) -> Dict[str, Any]:
        """
        Fetches market overview for a specific coin.
        """
        if coin_id in overview_cache:
            return overview_cache[coin_id]

        async with httpx.AsyncClient() as client:
            url = f"{BASE_URL}/coins/{coin_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "false",
                "developer_data": "false",
                "sparkline": "false"
            }
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            market_data = data.get("market_data", {})

            result = {
                "name": data.get("name"),
                "symbol": data.get("symbol", "").upper(),
                "current_price": market_data.get("current_price", {}).get("usd", 0),
                "market_cap": market_data.get("market_cap", {}).get("usd", 0),
                "volume_24h": market_data.get("total_volume", {}).get("usd", 0),
                "price_change_24h": market_data.get("price_change_percentage_24h", 0),
                "price_change_7d": market_data.get("price_change_percentage_7d", 0),
                "ath": market_data.get("ath", {}).get("usd", 0),
                "atl": market_data.get("atl", {}).get("usd", 0),
                "circulating_supply": market_data.get("circulating_supply", 0)
            }

            overview_cache[coin_id] = result
            return result
