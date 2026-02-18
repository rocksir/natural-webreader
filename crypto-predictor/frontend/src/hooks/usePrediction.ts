import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { PredictionResponse } from '../types'

const API_BASE = '/api'

export const usePrediction = (coinId: string) => {
  return useQuery<PredictionResponse>({
    queryKey: ['prediction', coinId],
    queryFn: async () => {
      const { data } = await axios.get(`${API_BASE}/prediction/signals`, {
        params: { coin_id: coinId }
      })
      return data
    },
    refetchInterval: 60000,
  })
}
