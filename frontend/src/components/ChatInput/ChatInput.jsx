import React, { useState } from 'react';
import { Send, Sliders, Sparkles, Loader2 } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const ChatInput = ({ onSendMessage, loading }) => {
  const { settings, setSettings } = useApp();
  const [query, setQuery] = useState('');
  const [showParams, setShowParams] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;
    onSendMessage(query, settings.topK, settings.alpha);
    setQuery('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const samplePrompts = [
    'What is the core architecture of the Adaptive Living GraphRAG framework?',
    'How does the 4-tier Trust Engine compute source reliability?',
    'What entity relationships exist between ChromaDB and Neo4j?',
  ];

  return (
    <div className="space-y-3">
      {/* Sample Prompts Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 text-xs no-scrollbar">
        <Sparkles className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
        {samplePrompts.map((prompt, i) => (
          <button
            key={i}
            onClick={() => setQuery(prompt)}
            className="px-3 py-1.5 rounded-full bg-slate-900/80 hover:bg-slate-800 border border-slate-800/80 text-slate-300 text-[11px] whitespace-nowrap transition-colors shrink-0"
          >
            {prompt}
          </button>
        ))}
      </div>

      {/* Parameter Controls Panel (Top-K & Alpha) */}
      {showParams && (
        <div className="glass-panel p-4 rounded-xl border border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Top-K Chunks ({settings.topK})</span>
              <span className="text-slate-500">Vector Retrieval Limit</span>
            </div>
            <input
              type="range"
              min="1"
              max="20"
              value={settings.topK}
              onChange={(e) => setSettings({ ...settings, topK: parseInt(e.target.value) })}
              className="w-full accent-cyan-400 bg-slate-800 rounded-lg cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-slate-300 mb-1">
              <span>Hybrid Alpha ({settings.alpha})</span>
              <span className="text-slate-500">Dense vs Sparse Weight</span>
            </div>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={settings.alpha}
              onChange={(e) => setSettings({ ...settings, alpha: parseFloat(e.target.value) })}
              className="w-full accent-indigo-400 bg-slate-800 rounded-lg cursor-pointer"
            />
          </div>
        </div>
      )}

      {/* Query Input Box */}
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about ingested PDF documents & graph entities..."
          rows={2}
          disabled={loading}
          className="w-full bg-slate-900/90 border border-slate-800 focus:border-cyan-500/50 rounded-2xl py-3 pl-4 pr-24 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-cyan-500/50 resize-none transition-all"
        />

        <div className="absolute right-3 flex items-center gap-2">
          <button
            type="button"
            onClick={() => setShowParams(!showParams)}
            className={`p-2 rounded-xl border transition-colors ${
              showParams
                ? 'bg-cyan-500/20 border-cyan-500/40 text-cyan-300'
                : 'bg-slate-800/80 border-slate-700/80 text-slate-400 hover:text-slate-200'
            }`}
            title="Adjust Retrieval Parameters (Top-K / Alpha)"
          >
            <Sliders className="w-4 h-4" />
          </button>

          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="p-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold shadow-md shadow-indigo-500/20 transition-all"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin text-white" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </form>
    </div>
  );
};
