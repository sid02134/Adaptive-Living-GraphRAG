import React from 'react';
import { Menu, Activity, Cpu, Database, RefreshCw } from 'lucide-react';
import { useApp } from '../../context/AppContext';

export const Navbar = ({ setMobileOpen }) => {
  const { health, healthLoading, refreshHealth } = useApp();

  const isHealthy = health.status === 'healthy';

  return (
    <header className="sticky top-0 z-30 h-16 bg-[#0B0F17]/80 backdrop-blur-md border-b border-slate-800/80 px-4 sm:px-6 flex items-center justify-between">
      {/* Mobile Toggle & Page Title Area */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => setMobileOpen(true)}
          className="p-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 lg:hidden"
          aria-label="Open Mobile Menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
          <span className="font-semibold text-slate-200">Adaptive Living</span>
          <span>/</span>
          <span className="text-cyan-400 font-medium">Knowledge GraphRAG Framework</span>
        </div>
      </div>

      {/* Health Badges & Actions */}
      <div className="flex items-center gap-3">
        {/* Component Health Pills */}
        <div className="hidden md:flex items-center gap-2 bg-slate-900/90 border border-slate-800 rounded-xl px-3 py-1.5 text-xs">
          <div className="flex items-center gap-1.5 pr-2 border-r border-slate-800">
            <span
              className={`w-2 h-2 rounded-full ${
                isHealthy ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-amber-400'
              }`}
            />
            <span className="font-semibold text-slate-200 capitalize">
              {health.status || 'Checking'}
            </span>
          </div>

          <div className="flex items-center gap-3 text-slate-400 text-[11px]">
            <span className="flex items-center gap-1" title={health.components?.chromadb?.details}>
              <Database className="w-3.5 h-3.5 text-indigo-400" />
              ChromaDB:
              <span
                className={`font-semibold ${
                  health.components?.chromadb?.status === 'online'
                    ? 'text-emerald-400'
                    : 'text-amber-400'
                }`}
              >
                {health.components?.chromadb?.status || '—'}
              </span>
            </span>

            <span className="flex items-center gap-1" title={health.components?.neo4j?.details}>
              <Activity className="w-3.5 h-3.5 text-cyan-400" />
              Neo4j:
              <span
                className={`font-semibold ${
                  health.components?.neo4j?.status === 'online'
                    ? 'text-emerald-400'
                    : 'text-amber-400'
                }`}
              >
                {health.components?.neo4j?.status || '—'}
              </span>
            </span>

            <span className="flex items-center gap-1" title={health.components?.ollama?.details}>
              <Cpu className="w-3.5 h-3.5 text-purple-400" />
              Ollama:
              <span
                className={`font-semibold ${
                  health.components?.ollama?.status === 'online'
                    ? 'text-emerald-400'
                    : 'text-rose-400'
                }`}
              >
                {health.components?.ollama?.status || '—'}
              </span>
            </span>
          </div>
        </div>

        {/* Refresh Health Button */}
        <button
          onClick={refreshHealth}
          disabled={healthLoading}
          className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700 transition-all text-xs flex items-center gap-1.5"
          title="Refresh System Health"
        >
          <RefreshCw className={`w-4 h-4 ${healthLoading ? 'animate-spin text-cyan-400' : ''}`} />
          <span className="hidden sm:inline">Refresh</span>
        </button>
      </div>
    </header>
  );
};
