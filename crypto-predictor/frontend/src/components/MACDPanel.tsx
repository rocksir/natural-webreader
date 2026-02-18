import React from 'react'
import {
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from 'recharts'

interface Props {
  data: any[];
  isLoading: boolean;
}

export const MACDPanel: React.FC<Props> = ({ data, isLoading }) => {
  if (isLoading) return <div className="h-full bg-panel animate-pulse" />

  return (
    <div className="w-full h-full">
      <div className="text-[10px] text-gray-400 mb-1 px-2 flex justify-between">
        <span>MACD (12, 26, 9)</span>
        <div className="space-x-2">
          <span className="text-[#00cfff]">MACD</span>
          <span className="text-[#f5a623]">Signal</span>
        </div>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e2d3d" vertical={false} />
          <XAxis dataKey="time" hide />
          <YAxis stroke="#4b5563" fontSize={8} orientation="right" />
          <Bar dataKey="macd_hist">
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.macd_hist >= 0 ? '#00ff8844' : '#ff3d5a44'}
              />
            ))}
          </Bar>
          <Line
            type="monotone"
            dataKey="macd"
            stroke="#00cfff"
            dot={false}
            strokeWidth={1}
            isAnimationActive={false}
          />
          <Line
            type="monotone"
            dataKey="macd_signal"
            stroke="#f5a623"
            dot={false}
            strokeWidth={1}
            isAnimationActive={false}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
