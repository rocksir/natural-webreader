export interface OHLCVData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  rsi?: number;
  macd?: number;
  macd_signal?: number;
  macd_hist?: number;
  bb_upper?: number;
  bb_lower?: number;
  bb_middle?: number;
}

export interface MarketOHLCVResponse {
  symbol: string;
  prices: OHLCVData[];
}

export interface MarketOverviewResponse {
  name: string;
  symbol: string;
  current_price: number;
  market_cap: number;
  volume_24h: number;
  price_change_24h: number;
  price_change_7d: number;
  ath: number;
  atl: number;
  circulating_supply: number;
}

export interface SignalDetail {
  indicator: string;
  value: number;
  signal: string;
  direction: 'bull' | 'bear' | 'neutral';
  weight: number;
}

export interface PriceRange {
  low: number;
  mid: number;
  high: number;
}

export interface PredictionResponse {
  overall_signal: 'STRONG BUY' | 'BUY' | 'NEUTRAL' | 'SELL' | 'STRONG SELL';
  confidence: number;
  predicted_direction: 'UP' | 'DOWN' | 'SIDEWAYS';
  predicted_price_range: PriceRange;
  horizon: string;
  signals: SignalDetail[];
  summary: string;
}
