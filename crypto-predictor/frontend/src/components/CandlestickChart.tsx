import React from 'react'
import {
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Bar,
  Cell,
  ReferenceLine
} from 'recharts'
import { OHLCVData } from '../types'
import { format } from 'date-fns'

interface Props {
  data: OHLCVData[];
  isLoading: boolean;
}

const Candlestick = (props: any) => {
  const { x, y, width, height, open, close, high, low } = props;
  const isUp = close >= open;
  const color = isUp ? '#00ff88' : '#ff3d5a';

  // props.y and props.height are for the range [low, high] if we use that as dataKey
  // but we can compute the body relative to the high/low range
  const ratio = height / (high - low);
  const bodyY = y + (high - Math.max(open, close)) * ratio;
  const bodyHeight = Math.abs(open - close) * ratio;

  return (
    <g>
      {/* Wick */}
      <line
        x1={x + width / 2}
        y1={y}
        x2={x + width / 2}
        y2={y + height}
        stroke={color}
        strokeWidth={1}
      />
      {/* Body */}
      <rect
        x={x}
        y={bodyY}
        width={width}
        height={Math.max(bodyHeight, 1)} // ensure at least 1px height
        fill={color}
      />
    </g>
  );
};

export const CandlestickChart: React.FC<Props> = ({ data, isLoading }) => {
  if (isLoading) {
    return <div className="w-full h-full bg-panel animate-pulse" />
  }

  const chartData = data.map(d => ({
    ...d,
    ohlc: [d.low, d.high, d.open, d.close] // Recharts Bar expects array for custom shape data access sometimes
  }));

  return (
    <div className="w-full h-full flex flex-col">
      <div className="flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e2d3d" vertical={false} />
            <XAxis
              dataKey="time"
              tickFormatter={(unix) => format(new Date(unix), 'MM/dd')}
              stroke="#4b5563"
              fontSize={10}
            />
            <YAxis
              domain={['auto', 'auto']}
              orientation="right"
              stroke="#4b5563"
              fontSize={10}
              tickFormatter={(val) => `$${val.toLocaleString()}`}
            />
            <Tooltip
              contentStyle={{ backgroundColor: '#0d1117', border: '1px solid #1e2d3d' }}
              labelFormatter={(unix) => format(new Date(unix), 'yyyy-MM-dd HH:mm')}
              itemStyle={{ fontSize: '12px' }}
            />
            <Bar
              dataKey="ohlc"
              shape={<Candlestick />}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
      <div className="h-24">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={data}>
            <XAxis dataKey="time" hide />
            <YAxis hide />
            <Bar dataKey="volume">
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={index > 0 && data[index].close >= data[index-1].close ? '#00ff8844' : '#ff3d5a44'}
                />
              ))}
            </Bar>
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
