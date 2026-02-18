import React from 'react'
import { clsx } from 'clsx'

interface Props {
  signal: string;
  confidence: number;
}

export const PredictionBadge: React.FC<Props> = ({ signal, confidence }) => {
  const isBull = signal.includes('BUY')
  const isBear = signal.includes('SELL')

  return (
    <div className={clsx(
      "p-4 border-2 flex flex-col items-center justify-center relative overflow-hidden",
      isBull ? "border-bull bg-bull/5 neon-glow-green" : isBear ? "border-bear bg-bear/5 neon-glow-red" : "border-neutral bg-neutral/5"
    )}>
      <div className="text-[10px] uppercase tracking-widest mb-1 text-gray-400">System Forecast</div>
      <div className={clsx(
        "text-2xl font-display font-bold tracking-tighter",
        isBull ? "text-bull" : isBear ? "text-bear" : "text-neutral"
      )}>
        {signal}
      </div>
      <div className="mt-2 flex items-center">
        <div className="w-24 h-1 bg-gray-800 rounded-full mr-2 overflow-hidden">
          <div
            className={clsx("h-full", isBull ? "bg-bull" : isBear ? "bg-bear" : "bg-neutral")}
            style={{ width: `${confidence}%` }}
          />
        </div>
        <span className="text-xs font-bold">{confidence.toFixed(1)}% CF</span>
      </div>
    </div>
  )
}
