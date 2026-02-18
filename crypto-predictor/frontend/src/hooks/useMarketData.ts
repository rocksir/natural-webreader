import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { MarketOHLCVResponse, MarketOverviewResponse } from '../types'

const API_BASE = '/api'

export const useOHLCV = (coinId: string, days: string) => {
  return useQuery<MarketOHLCVResponse>({
    queryKey: ['ohlcv', coinId, days],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/market/ohlcv`, {
        params: { coin_id: coinId, days }
      })
      return data
    },
    refetchInterval: 60000,
  })
}

export const useMarketOverview = (coinId: string) => {
  return useQuery<MarketOverviewResponse>({
    queryKey: ['overview', coinId],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/market/overview`, {
        params: { coin_id: coinId }
      })
      return data
    },
    refetchInterval: 60000,
  })
}
