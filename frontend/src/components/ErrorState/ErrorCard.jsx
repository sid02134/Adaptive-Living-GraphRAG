import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export const ErrorCard = ({ title = 'Failed to load data', message, onRetry }) => {
  return (
    <div className="glass-panel p-6 rounded-2xl border border-rose-800/60 bg-rose-950/20 text-center flex flex-col items-center justify-center space-y-3">
      <div className="p-3 rounded-2xl bg-rose-500/10 border border-rose-500/20 text-rose-400">
        <AlertCircle className="w-8 h-8" />
      </div>
      <div>
        <h4 className="font-bold text-sm text-slate-200">{title}</h4>
        <p className="text-xs text-rose-300/80 mt-1 max-w-md">{message || 'An error occurred while connecting to the backend API server.'}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="mt-2 px-4 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs font-semibold text-slate-200 flex items-center gap-2 transition-all"
        >
          <RefreshCw className="w-3.5 h-3.5 text-cyan-400" />
          Retry Request
        </button>
      )}
    </div>
  );
};
