import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  ReferenceLine
} from 'recharts'
import { OHLCVData } from '../types'

interface Props {
  data: any[]; // Data with indicators
  isLoading: boolean;
}

export const RSIPanel: React.FC<Props> = ({ data, isLoading }) => {
  if (isLoading) return <div className="h-full bg-panel animate-pulse" />

  return (
    <div className="w-full h-full">
      <div className="text-[10px] text-gray-400 mb-1 px-2 flex justify-between">
        <span>RSI (14)</span>
        <span className="text-info">{data[data.length - 1]?.rsi?.toFixed(2)}</span>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e2d3d" vertical={false} />
          <XAxis dataKey="time" hide />
          <YAxis domain={[0, 100]} ticks={[30, 70]} stroke="#4b5563" fontSize={8} orientation="right" />
          <ReferenceLine y={70} stroke="#ff3d5a" strokeDasharray="3 3" />
          <ReferenceLine y={30} stroke="#00ff88" strokeDasharray="3 3" />
          <Line
            type="monotone"
            dataKey="rsi"
            stroke="#00cfff"
            dot={false}
            strokeWidth={1.5}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
