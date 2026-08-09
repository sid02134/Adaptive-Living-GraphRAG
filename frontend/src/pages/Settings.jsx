import React from 'react';
import { Settings as SettingsIcon, Sliders, Cpu, Database, Server, Info, Save } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const Settings = () => {
  const { settings, setSettings, health } = useApp();

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-100 tracking-tight flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-cyan-400" />
          System Settings & Parameter Configurations
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Informational overview and runtime parameter controls for LLM, vector retrieval, and backend endpoints.
        </p>
      </div>

      <div className="space-y-6">
        {/* LLM Section */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2 pb-3 border-b border-slate-800">
            <Cpu className="w-4 h-4 text-purple-400" />
            LLM Synthesis Configuration
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 font-semibold mb-1">Ollama LLM Model</label>
              <input
                type="text"
                value={settings.llmModel}
                disabled
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-300 font-mono"
              />
              <span className="text-[10px] text-slate-500 mt-1 block">Local Ollama Llama 3 model backend</span>
            </div>

            <div>
              <label className="block text-slate-400 font-semibold mb-1">Sampling Temperature ({settings.temperature})</label>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={settings.temperature}
                onChange={(e) => setSettings({ ...settings, temperature: parseFloat(e.target.value) })}
                className="w-full accent-purple-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <span className="text-[10px] text-slate-500 mt-1 block">Lower values produce strictly factual RAG answers</span>
            </div>
          </div>
        </div>

        {/* Retrieval Parameters */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2 pb-3 border-b border-slate-800">
            <Sliders className="w-4 h-4 text-cyan-400" />
            GraphRAG Hybrid Retrieval Parameters
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 font-semibold mb-1">Default Top-K Chunks ({settings.topK})</label>
              <input
                type="range"
                min="1"
                max="20"
                value={settings.topK}
                onChange={(e) => setSettings({ ...settings, topK: parseInt(e.target.value) })}
                className="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <span className="text-[10px] text-slate-500 mt-1 block">Number of ChromaDB context chunks retrieved per query</span>
            </div>

            <div>
              <label className="block text-slate-400 font-semibold mb-1">Hybrid Alpha Weight ({settings.alpha})</label>
              <input
                type="range"
                min="0.0"
                max="1.0"
                step="0.05"
                value={settings.alpha}
                onChange={(e) => setSettings({ ...settings, alpha: parseFloat(e.target.value) })}
                className="w-full accent-indigo-400 bg-slate-800 rounded-lg cursor-pointer"
              />
              <span className="text-[10px] text-slate-500 mt-1 block">1.0 = Dense Vector match, 0.0 = Sparse BM25 text match</span>
            </div>
          </div>
        </div>

        {/* Ingestion Parameters */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2 pb-3 border-b border-slate-800">
            <Database className="w-4 h-4 text-indigo-400" />
            Module 1 Ingestion Parameters
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 font-semibold mb-1">Chunk Character Size</label>
              <input
                type="number"
                value={settings.chunkSize}
                disabled
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-300 font-mono"
              />
            </div>

            <div>
              <label className="block text-slate-400 font-semibold mb-1">Chunk Overlap Characters</label>
              <input
                type="number"
                value={settings.chunkOverlap}
                disabled
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-slate-300 font-mono"
              />
            </div>
          </div>
        </div>

        {/* System Endpoint Details */}
        <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2 pb-3 border-b border-slate-800">
            <Server className="w-4 h-4 text-emerald-400" />
            FastAPI Server Connection
          </h3>

          <div className="text-xs space-y-2">
            <div className="flex justify-between items-center bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400">Backend API URL</span>
              <code className="text-cyan-300 font-bold">{settings.backendUrl}</code>
            </div>
            <div className="flex justify-between items-center bg-slate-950 p-3 rounded-xl border border-slate-800">
              <span className="text-slate-400">API Health Status</span>
              <span className="text-emerald-400 font-bold capitalize">{health.status}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
