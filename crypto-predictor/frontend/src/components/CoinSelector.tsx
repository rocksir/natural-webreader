import React from 'react'
import { useAppStore } from '../store/appStore'

const COINS = [
  { id: 'bitcoin', name: 'Bitcoin', symbol: 'BTC' },
  { id: 'ethereum', name: 'Ethereum', symbol: 'ETH' },
  { id: 'binancecoin', name: 'BNB', symbol: 'BNB' },
  { id: 'solana', name: 'Solana', symbol: 'SOL' },
  { id: 'ripple', name: 'XRP', symbol: 'XRP' },
  { id: 'cardano', name: 'Cardano', symbol: 'ADA' },
  { id: 'dogecoin', name: 'Dogecoin', symbol: 'DOGE' },
  { id: 'avalanche-2', name: 'Avalanche', symbol: 'AVAX' },
  { id: 'polkadot', name: 'Polkadot', symbol: 'DOT' },
  { id: 'chainlink', name: 'Chainlink', symbol: 'LINK' },
]

export const CoinSelector: React.FC = () => {
  const { selectedCoin, setSelectedCoin } = useAppStore()

  return (
    <select
      value={selectedCoin}
      onChange={(e) => setSelectedCoin(e.target.value)}
      className="bg-panel border border-border text-white px-3 py-1 outline-none focus:border-info font-display"
    >
      {COINS.map((coin) => (
        <option key={coin.id} value={coin.id}>
          {coin.name} ({coin.symbol})
        </option>
      ))}
    </select>
  )
}
