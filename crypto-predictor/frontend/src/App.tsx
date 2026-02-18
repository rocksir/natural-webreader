import React, { useState, useEffect } from 'react'
import { CoinSelector } from './components/CoinSelector'
import { TimeframeSelector } from './components/TimeframeSelector'
import { MarketStats } from './components/MarketStats'
import { CandlestickChart } from './components/CandlestickChart'
import { RSIPanel } from './components/RSIPanel'
import { MACDPanel } from './components/MACDPanel'
import { PredictionBadge } from './components/PredictionBadge'
import { SignalCard } from './components/SignalCard'
import { ScalperPanel } from './components/ScalperPanel'
import { useAppStore } from './store/appStore'
import { clsx } from 'clsx'
import { useOHLCV } from './hooks/useMarketData'
import { usePrediction } from './hooks/usePrediction'
import { Activity, Clock, ShieldAlert, Zap } from 'lucide-react'

const App: React.FC = () => {
  const { selectedCoin, selectedTimeframe } = useAppStore()
  const { data: ohlcvData, isLoading: isLoadingOHLCV } = useOHLCV(selectedCoin, selectedTimeframe)
  const { data: predictionData, isLoading: isLoadingPrediction } = usePrediction(selectedCoin)

  const [countdown, setCountdown] = useState(60)
  const [showDisclaimer, setShowDisclaimer] = useState(true)
  const [activeTab, setActiveTab] = useState<'signals' | 'scalper'>('signals')

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => (prev <= 1 ? 60 : prev - 1))
    }, 1000)
    return () => clearInterval(timer)
  }, [selectedCoin])

  // Process data for indicators if needed locally, but backend does it.
  // We'll just pass the data to panels.

  return (
    <div className="min-h-screen flex flex-col overflow-hidden relative">
      <div className="scanline" />

      {/* Header */}
      <header className="h-14 border-b border-border flex items-center justify-between px-6 bg-background/80 backdrop-blur-md z-20">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-info rounded-sm flex items-center justify-center">
              <Zap size={20} className="text-black" />
            </div>
            <span className="font-display font-bold text-xl tracking-tighter">CRYPTO<span className="text-info">PREDICTOR</span></span>
          </div>
          <div className="h-6 w-px bg-border mx-2" />
          <CoinSelector />
          <TimeframeSelector />
        </div>

        <div className="flex items-center space-x-6">
          <div className="flex items-center text-xs text-gray-400">
            <Clock size={14} className="mr-2" />
            <span>{new Date().toLocaleTimeString()} UTC</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-bull rounded-full animate-pulse" />
            <span className="text-[10px] text-bull uppercase font-bold tracking-widest">Live Data</span>
            <span className="text-[10px] text-gray-500 font-mono">REFRESH IN {countdown}S</span>
          </div>
        </div>
      </header>

      <MarketStats />

      {/* Main Dashboard */}
      <main className="flex-1 flex flex-col md:flex-row p-4 gap-4 overflow-hidden">
        {/* Left Side: Charts */}
        <div className="flex-[3] flex flex-col gap-4 min-h-[500px]">
          <div className="flex-1 bg-panel/50 border border-border p-4 relative overflow-hidden">
             <div className="absolute top-2 left-4 text-[10px] text-gray-500 uppercase z-10">Price Chart / Volume</div>
             <CandlestickChart data={ohlcvData?.prices || []} isLoading={isLoadingOHLCV} />
          </div>
          <div className="h-48 flex gap-4">
            <div className="flex-1 bg-panel/50 border border-border p-4">
              <RSIPanel data={ohlcvData?.prices || []} isLoading={isLoadingOHLCV} />
            </div>
            <div className="flex-1 bg-panel/50 border border-border p-4">
              <MACDPanel data={ohlcvData?.prices || []} isLoading={isLoadingOHLCV} />
            </div>
          </div>
        </div>

        {/* Right Side: Prediction & Signals */}
        <div className="flex-1 flex flex-col gap-4 min-w-[320px] overflow-hidden">
          {isLoadingPrediction ? (
            <div className="flex-1 bg-panel/50 border border-border p-6 animate-pulse" />
          ) : predictionData ? (
            <>
              <PredictionBadge
                signal={predictionData.overall_signal}
                confidence={predictionData.confidence}
              />

              <div className="bg-panel/30 border border-border p-4">
                <div className="text-[10px] text-gray-400 uppercase mb-2">Target Range (24h)</div>
                <div className="flex justify-between items-end">
                  <div className="flex flex-col">
                    <span className="text-[10px] text-gray-500">LOW</span>
                    <span className="text-sm font-bold text-bear">${predictionData.predicted_price_range.low.toLocaleString()}</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <span className="text-[10px] text-gray-500">ESTIMATED</span>
                    <span className="text-lg font-bold text-info">${predictionData.predicted_price_range.mid.toLocaleString()}</span>
                  </div>
                  <div className="flex flex-col items-end">
                    <span className="text-[10px] text-gray-500">HIGH</span>
                    <span className="text-sm font-bold text-bull">${predictionData.predicted_price_range.high.toLocaleString()}</span>
                  </div>
                </div>
              </div>

              <div className="flex-1 bg-panel/20 border border-border flex flex-col overflow-hidden">
                <div className="flex border-b border-border">
                  <button
                    onClick={() => setActiveTab('signals')}
                    className={clsx(
                      "flex-1 py-2 text-[10px] uppercase font-bold tracking-widest transition-colors",
                      activeTab === 'signals' ? "bg-info/10 text-info border-b-2 border-info" : "text-gray-500 hover:text-gray-300"
                    )}
                  >
                    Signals
                  </button>
                  <button
                    onClick={() => setActiveTab('scalper')}
                    className={clsx(
                      "flex-1 py-2 text-[10px] uppercase font-bold tracking-widest transition-colors",
                      activeTab === 'scalper' ? "bg-bull/10 text-bull border-b-2 border-bull" : "text-gray-500 hover:text-gray-300"
                    )}
                  >
                    Scalper
                  </button>
                </div>

                <div className="flex-1 p-4 overflow-hidden flex flex-col">
                  {activeTab === 'signals' ? (
                    <>
                      <div className="flex-1 overflow-y-auto pr-1">
                        {predictionData.signals.map((signal, idx) => (
                          <SignalCard key={signal.indicator} signal={signal} index={idx} />
                        ))}
                      </div>
                      <div className="mt-4 pt-3 border-t border-border">
                         <p className="text-[10px] leading-relaxed text-gray-400 italic">
                           {predictionData.summary}
                         </p>
                      </div>
                    </>
                  ) : (
                    <ScalperPanel />
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center border border-border bg-panel">
               <span className="text-gray-500 uppercase text-xs">Error loading prediction</span>
            </div>
          )}
        </div>
      </main>

      {/* Footer Disclaimer */}
      {showDisclaimer && (
        <div className="bg-bear/10 border-t border-bear/30 px-6 py-2 flex items-center justify-between z-30">
          <div className="flex items-center">
            <ShieldAlert size={14} className="text-bear mr-2" />
            <p className="text-[10px] text-gray-300">
              <span className="font-bold text-bear mr-1">DISCLAIMER:</span>
              This tool is for educational purposes only. Crypto markets are highly volatile. Never invest based solely on algorithmic signals.
            </p>
          </div>
          <button
            onClick={() => setShowDisclaimer(false)}
            className="text-[10px] uppercase font-bold hover:text-white text-gray-500 transition-colors"
          >
            DISMISS
          </button>
        </div>
      )}

      <footer className="h-6 border-t border-border px-6 flex items-center justify-between bg-background text-[10px] text-gray-600">
        <span>CRYPTO-PREDICTOR V0.1.0-BETA</span>
        <span>MARKET DATA BY COINGECKO</span>
        <div className="flex space-x-4">
          <span className="text-bull">STABLE CONNECTION</span>
          <span className="text-info">API: HEALTHY</span>
        </div>
      </footer>
    </div>
  )
}

export default App
