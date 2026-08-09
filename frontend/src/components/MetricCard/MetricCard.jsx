import React from 'react';

export const MetricCard = ({ title, value, unit, subtitle, icon: Icon, trend, color = 'indigo' }) => {
  const colorMap = {
    indigo: {
      iconBg: 'bg-indigo-500/10 border-indigo-500/20 text-indigo-400',
      glow: 'group-hover:border-indigo-500/30',
    },
    cyan: {
      iconBg: 'bg-cyan-500/10 border-cyan-500/20 text-cyan-400',
      glow: 'group-hover:border-cyan-500/30',
    },
    purple: {
      iconBg: 'bg-purple-500/10 border-purple-500/20 text-purple-400',
      glow: 'group-hover:border-purple-500/30',
    },
    emerald: {
      iconBg: 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400',
      glow: 'group-hover:border-emerald-500/30',
    },
    amber: {
      iconBg: 'bg-amber-500/10 border-amber-500/20 text-amber-400',
      glow: 'group-hover:border-amber-500/30',
    },
  };

  const scheme = colorMap[color] || colorMap.indigo;

  return (
    <div className={`group relative glass-panel rounded-2xl p-5 transition-all duration-300 ${scheme.glow}`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && (
          <div className={`p-2.5 rounded-xl border ${scheme.iconBg}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="mt-3 flex items-baseline gap-1.5">
        <span className="text-2xl sm:text-3xl font-extrabold text-slate-100 font-mono tracking-tight">
          {value !== undefined && value !== null ? value : '—'}
        </span>
        {unit && <span className="text-xs text-slate-400 font-medium">{unit}</span>}
      </div>

      {subtitle && (
        <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
          <span>{subtitle}</span>
          {trend && (
            <span className="text-emerald-400 font-semibold flex items-center gap-0.5">
              ↑ {trend}
            </span>
          )}
        </div>
      )}
    </div>
  );
};
