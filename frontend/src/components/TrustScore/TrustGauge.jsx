import React from 'react';

export const TrustGauge = ({ score = 88.5, confidenceLevel = 'High Trust', size = 'md' }) => {
  const percentage = Math.min(100, Math.max(0, score));
  const radius = size === 'lg' ? 70 : 50;
  const strokeWidth = size === 'lg' ? 12 : 8;
  const normalizedRadius = radius - strokeWidth / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const getColor = (val) => {
    if (val >= 85) return { stroke: '#34D399', text: 'text-emerald-400', glow: 'drop-shadow-[0_0_12px_rgba(52,211,153,0.4)]' };
    if (val >= 70) return { stroke: '#38BDF8', text: 'text-cyan-400', glow: 'drop-shadow-[0_0_12px_rgba(56,189,248,0.4)]' };
    if (val >= 50) return { stroke: '#FBBF24', text: 'text-amber-400', glow: 'drop-shadow-[0_0_12px_rgba(251,191,36,0.4)]' };
    return { stroke: '#F43F5E', text: 'text-rose-400', glow: 'drop-shadow-[0_0_12px_rgba(244,63,94,0.4)]' };
  };

  const theme = getColor(percentage);
  const svgSize = radius * 2;

  return (
    <div className="flex flex-col items-center justify-center p-2">
      <div className="relative flex items-center justify-center">
        <svg height={svgSize} width={svgSize} className={`transform -rotate-90 ${theme.glow}`}>
          {/* Background circle */}
          <circle
            stroke="rgba(255, 255, 255, 0.08)"
            fill="transparent"
            strokeWidth={strokeWidth}
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
          {/* Progress circle */}
          <circle
            stroke={theme.stroke}
            fill="transparent"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference + ' ' + circumference}
            style={{ strokeDashoffset }}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
            r={normalizedRadius}
            cx={radius}
            cy={radius}
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center text-center">
          <span className={`font-mono font-extrabold ${size === 'lg' ? 'text-4xl' : 'text-2xl'} ${theme.text}`}>
            {percentage.toFixed(1)}%
          </span>
          <span className="text-[10px] uppercase font-semibold tracking-wider text-slate-400 mt-0.5">
            Trust Score
          </span>
        </div>
      </div>

      {confidenceLevel && (
        <span className="mt-3 px-3 py-1 rounded-full text-xs font-semibold bg-slate-900 border border-slate-800 text-cyan-300">
          {confidenceLevel}
        </span>
      )}
    </div>
  );
};
