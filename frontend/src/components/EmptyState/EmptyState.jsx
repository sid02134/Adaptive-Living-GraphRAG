import React from 'react';
import { Database } from 'lucide-react';

export const EmptyState = ({ title = 'No records found', message, icon: Icon = Database }) => {
  return (
    <div className="glass-panel p-8 rounded-2xl border border-slate-800 text-center flex flex-col items-center justify-center space-y-3">
      <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-slate-500">
        <Icon className="w-8 h-8" />
      </div>
      <div>
        <h4 className="font-bold text-sm text-slate-200">{title}</h4>
        <p className="text-xs text-slate-400 mt-1 max-w-sm">{message || 'No data is currently available in this section.'}</p>
      </div>
    </div>
  );
};
