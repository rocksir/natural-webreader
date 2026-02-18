import React from 'react'
import { useAppStore } from '../store/appStore'
import { clsx } from 'clsx'

const TIMEFRAMES = [
  { label: '1D', value: '1' },
  { label: '7D', value: '7' },
  { label: '14D', value: '14' },
  { label: '30D', value: '30' },
  { label: '90D', value: '90' },
]

export const TimeframeSelector: React.FC = () => {
  const { selectedTimeframe, setSelectedTimeframe } = useAppStore()

  return (
    <div className="flex border border-border">
      {TIMEFRAMES.map((tf) => (
        <button
          key={tf.value}
          onClick={() => setSelectedTimeframe(tf.value)}
          className={clsx(
            'px-3 py-1 text-xs transition-colors',
            selectedTimeframe === tf.value
              ? 'bg-info text-black font-bold'
              : 'hover:bg-panel'
          )}
        >
          {tf.label}
        </button>
      ))}
    </div>
  )
}
