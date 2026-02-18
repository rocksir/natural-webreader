import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { useAppStore } from '../store/appStore'
import { Play, Square, Key, ShieldCheck, Terminal as TerminalIcon } from 'lucide-react'
import { clsx } from 'clsx'

export const ScalperPanel: React.FC = () => {
  const { isScalperRunning, setScalperRunning, scalperLogs, setScalperLogs } = useAppStore()
  const [exchangeId, setExchangeId] = useState('binance')
  const [apiKey, setApiKey] = useState('')
  const [secret, setSecret] = useState('')
  const [testnet, setTestnet] = useState(true)
  const [symbol, setSymbol] = useState('BTC/USDT')

  useEffect(() => {
    let interval: any;
    if (isScalperRunning) {
      interval = setInterval(async () => {
        try {
          const { data } = await axios.get('/api/trading/status')
          setScalperLogs(data.logs)
          setScalperRunning(data.is_running)
        } catch (e) {
          console.error("Failed to fetch scalper status", e)
        }
      }, 5000)
    }
    return () => clearInterval(interval)
  }, [isScalperRunning])

  const handleStart = async () => {
    try {
      const { data } = await axios.post('/api/trading/start', {
        exchange_id: exchangeId,
        api_key: apiKey,
        secret: secret,
        testnet: testnet
      }, { params: { symbol } })
      setScalperRunning(true)
      setScalperLogs(data.status.logs)
    } catch (e: any) {
      alert(e.response?.data?.detail || "Failed to start scalper")
    }
  }

  const handleStop = async () => {
    try {
      await axios.post('/api/trading/stop')
      setScalperRunning(false)
    } catch (e) {
      console.error("Failed to stop scalper", e)
    }
  }

  return (
    <div className="flex flex-col h-full gap-4">
      {/* Config Form */}
      <div className="bg-panel/40 border border-border p-4">
        <div className="text-[10px] text-gray-400 uppercase mb-3 flex items-center">
          <Key size={12} className="mr-1" />
          Exchange Connectivity
        </div>

        {!isScalperRunning ? (
          <div className="space-y-3">
            <div className="flex gap-2">
              <select
                value={exchangeId}
                onChange={(e) => setExchangeId(e.target.value)}
                className="bg-background border border-border text-xs px-2 py-1 flex-1 outline-none"
              >
                <option value="binance">Binance</option>
                <option value="bybit">Bybit</option>
                <option value="okx">OKX</option>
                <option value="kucoin">KuCoin</option>
              </select>
              <input
                type="text"
                placeholder="Symbol (e.g. BTC/USDT)"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
                className="bg-background border border-border text-xs px-2 py-1 flex-1 outline-none"
              />
            </div>
            <input
              type="password"
              placeholder="API Key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              className="w-full bg-background border border-border text-xs px-2 py-1 outline-none"
            />
            <input
              type="password"
              placeholder="Secret"
              value={secret}
              onChange={(e) => setSecret(e.target.value)}
              className="w-full bg-background border border-border text-xs px-2 py-1 outline-none"
            />
            <div className="flex items-center justify-between">
              <label className="flex items-center text-[10px] text-gray-400 cursor-pointer">
                <input
                  type="checkbox"
                  checked={testnet}
                  onChange={(e) => setTestnet(e.target.checked)}
                  className="mr-2"
                />
                TESTNET MODE
              </label>
              <button
                onClick={handleStart}
                disabled={!apiKey || !secret}
                className="bg-bull text-black text-[10px] font-bold px-4 py-1 flex items-center disabled:opacity-50"
              >
                <Play size={10} className="mr-1 fill-current" />
                INITIATE SCALPER
              </button>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-between p-2 border border-bull/30 bg-bull/5">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-bull rounded-full animate-pulse mr-2" />
              <span className="text-[10px] text-bull font-bold uppercase">Scalper Active: {symbol}</span>
            </div>
            <button
              onClick={handleStop}
              className="bg-bear text-white text-[10px] font-bold px-3 py-1 flex items-center"
            >
              <Square size={10} className="mr-1 fill-current" />
              TERMINATE
            </button>
          </div>
        )}
      </div>

      {/* Real-time Logs */}
      <div className="flex-1 bg-black/40 border border-border flex flex-col overflow-hidden">
        <div className="text-[10px] text-gray-400 uppercase p-2 border-b border-border flex items-center">
          <TerminalIcon size={12} className="mr-1" />
          Execution Logs
        </div>
        <div className="flex-1 overflow-y-auto p-2 font-mono text-[9px] leading-relaxed scrollbar-hide">
          {scalperLogs.length === 0 ? (
            <div className="text-gray-600 italic">Waiting for connection...</div>
          ) : (
            scalperLogs.map((log, i) => (
              <div key={i} className={clsx(
                "mb-1",
                log.includes("SIGNAL") ? "text-bull" : log.includes("Error") ? "text-bear" : "text-gray-400"
              )}>
                {log}
              </div>
            )).reverse()
          )}
        </div>
      </div>

      <div className="bg-info/5 border border-info/20 p-2 flex items-start">
        <ShieldCheck size={14} className="text-info mr-2 mt-0.5" />
        <p className="text-[9px] text-gray-400 leading-tight">
          Keys are handled in-memory and never stored on disk. Using Testnet is highly recommended for strategy validation.
        </p>
      </div>
    </div>
  )
}
