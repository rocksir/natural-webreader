import React from 'react'
import { useMarketOverview } from '../hooks/useMarketData'
import { useAppStore } from '../store/appStore'
import { clsx } from 'clsx'

export const MarketStats: React.FC = () => {
  const { selectedCoin } = useAppStore()
  const { data, isLoading } = useMarketOverview(selectedCoin)

  if (isLoading || !data) {
    return <div className="h-12 w-full bg-panel animate-pulse" />
  }

  const formatCurrency = (val: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)

  const formatCompact = (val: number) =>
    new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 2 }).format(val)

  return (
    <div className="flex items-center space-x-8 py-2 px-4 bg-panel border-b border-border overflow-x-auto whitespace-nowrap">
      <div className="flex flex-col">
        <span className="text-[10px] text-gray-400 uppercase">Price</span>
        <span className="text-sm font-bold text-info">{formatCurrency(data.current_price)}</span>
      </div>
      <div className="flex flex-col">
        <span className="text-[10px] text-gray-400 uppercase">24h %</span>
        <span className={clsx(
          "text-sm font-bold",
          data.price_change_24h >= 0 ? "text-bull" : "text-bear"
        )}>
          {data.price_change_24h.toFixed(2)}%
        </span>
      </div>
      <div className="flex flex-col">
        <span className="text-[10px] text-gray-400 uppercase">Market Cap</span>
        <span className="text-sm font-bold">{formatCompact(data.market_cap)}</span>
      </div>
      <div className="flex flex-col">
        <span className="text-[10px] text-gray-400 uppercase">Volume (24h)</span>
        <span className="text-sm font-bold">{formatCompact(data.volume_24h)}</span>
      </div>
      <div className="flex flex-col">
        <span className="text-[10px] text-gray-400 uppercase">Circulating Supply</span>
        <span className="text-sm font-bold">{formatCompact(data.circulating_supply)} {data.symbol}</span>
      </div>
    </div>
  )
}
