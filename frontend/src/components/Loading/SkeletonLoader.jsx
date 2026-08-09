import React from 'react';

export const SkeletonLoader = ({ count = 3, type = 'card' }) => {
  return (
    <div className="space-y-3 animate-pulse">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="glass-panel p-4 rounded-xl border border-slate-800/80 bg-slate-900/50 flex items-center justify-between"
        >
          <div className="space-y-2 flex-1">
            <div className="h-4 bg-slate-800 rounded w-1/3" />
            <div className="h-3 bg-slate-800/60 rounded w-2/3" />
          </div>
          <div className="w-10 h-10 bg-slate-800 rounded-xl" />
        </div>
      ))}
    </div>
  );
};
