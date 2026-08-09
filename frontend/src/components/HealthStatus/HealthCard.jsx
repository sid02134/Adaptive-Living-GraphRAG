import React from 'react';
import { CheckCircle2, AlertTriangle, XCircle, HelpCircle } from 'lucide-react';

export const HealthCard = ({ name, status, details, icon: ComponentIcon }) => {
  const getStatusConfig = () => {
    switch (status?.toLowerCase()) {
      case 'online':
        return {
          badgeClass: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
          dotClass: 'bg-emerald-400',
          Icon: CheckCircle2,
          label: 'ONLINE',
        };
      case 'degraded':
        return {
          badgeClass: 'bg-amber-500/10 text-amber-400 border-amber-500/30',
          dotClass: 'bg-amber-400',
          Icon: AlertTriangle,
          label: 'DEGRADED',
        };
      case 'offline':
        return {
          badgeClass: 'bg-rose-500/10 text-rose-400 border-rose-500/30',
          dotClass: 'bg-rose-400',
          Icon: XCircle,
          label: 'OFFLINE',
        };
      default:
        return {
          badgeClass: 'bg-slate-500/10 text-slate-400 border-slate-500/30',
          dotClass: 'bg-slate-400',
          Icon: HelpCircle,
          label: 'UNKNOWN',
        };
    }
  };

  const config = getStatusConfig();
  const StatusIcon = config.Icon;

  return (
    <div className="glass-panel rounded-2xl p-4 flex flex-col justify-between border border-slate-800/80">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {ComponentIcon && (
            <div className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-cyan-400">
              <ComponentIcon className="w-5 h-5" />
            </div>
          )}
          <div>
            <h4 className="font-bold text-sm text-slate-200 capitalize">{name}</h4>
            <p className="text-[11px] text-slate-400 mt-0.5 truncate max-w-[180px]">
              {details || 'Component active'}
            </p>
          </div>
        </div>

        <span
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider border ${config.badgeClass}`}
        >
          <StatusIcon className="w-3.5 h-3.5" />
          {config.label}
        </span>
      </div>
    </div>
  );
};
