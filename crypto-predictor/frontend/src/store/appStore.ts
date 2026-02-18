import { create } from 'zustand'

interface AppState {
  selectedCoin: string;
  selectedTimeframe: string;
  isScalperRunning: boolean;
  scalperLogs: string[];
  setSelectedCoin: (coin: string) => void;
  setSelectedTimeframe: (timeframe: string) => void;
  setScalperRunning: (running: boolean) => void;
  setScalperLogs: (logs: string[]) => void;
}

export const useAppStore = create<AppState>((set) => ({
  selectedCoin: 'bitcoin',
  selectedTimeframe: '30', // days
  isScalperRunning: false,
  scalperLogs: [],
  setSelectedCoin: (coin) => set({ selectedCoin: coin }),
  setSelectedTimeframe: (timeframe) => set({ selectedTimeframe: timeframe }),
  setScalperRunning: (running) => set({ isScalperRunning: running }),
  setScalperLogs: (logs) => set({ scalperLogs: logs }),
}))
