import React from 'react'
import { SignalDetail } from '../types'
import { clsx } from 'clsx'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface Props {
  signal: SignalDetail;
  index: number;
}

export const SignalCard: React.FC<Props> = ({ signal, index }) => {
  return (
    <div
      className="flex items-center justify-between p-3 bg-panel border-l-2 mb-2 animate-in fade-in slide-in-from-right-4 duration-500"
      style={{
        borderLeftColor: signal.direction === 'bull' ? '#00ff88' : signal.direction === 'bear' ? '#ff3d5a' : '#f5a623',
        animationDelay: `${index * 100}ms`
      }}
    >
      <div className="flex flex-col">
        <span className="text-[10px] text-gray-400 uppercase">{signal.indicator}</span>
        <span className="text-xs font-bold">{signal.signal}</span>
      </div>
      <div className="flex items-center">
        <span className="text-[10px] mr-2 text-gray-500">{signal.value}</span>
        {signal.direction === 'bull' && <TrendingUp size={14} className="text-bull" />}
        {signal.direction === 'bear' && <TrendingDown size={14} className="text-bear" />}
        {signal.direction === 'neutral' && <Minus size={14} className="text-neutral" />}
      </div>
    </div>
  )
}
