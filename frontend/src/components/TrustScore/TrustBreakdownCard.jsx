import React from 'react';
import { Target, ShieldCheck, GitMerge, FileCheck } from 'lucide-react';

export const TrustBreakdownCard = ({ breakdown }) => {
  const metrics = [
    {
      name: 'Semantic Similarity',
      weight: '40%',
      value: breakdown?.semantic_similarity ?? 89.5,
      icon: Target,
      color: 'from-cyan-500 to-blue-500',
      description: 'ChromaDB vector embedding relevance match',
    },
    {
      name: 'Source Reliability',
      weight: '30%',
      value: breakdown?.source_reliability ?? 92.0,
      icon: ShieldCheck,
      color: 'from-emerald-500 to-teal-500',
      description: 'Ingested document authority & provenance integrity',
    },
    {
      name: 'Graph Consistency',
      weight: '20%',
      value: breakdown?.graph_consistency ?? 85.0,
      icon: GitMerge,
      color: 'from-purple-500 to-indigo-500',
      description: 'Neo4j entity relationship verification depth',
    },
    {
      name: 'Citation Coverage',
      weight: '10%',
      value: breakdown?.citation_coverage ?? 87.5,
      icon: FileCheck,
      color: 'from-amber-500 to-orange-500',
      description: 'Verifiable inline source attribution ratio',
    },
  ];

  return (
    <div className="space-y-4">
      {metrics.map((item) => {
        const Icon = item.icon;
        const score = typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0;

        return (
          <div key={item.name} className="glass-panel p-4 rounded-xl border border-slate-800/80">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
                  <Icon className="w-4 h-4 text-cyan-400" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-xs text-slate-200">{item.name}</span>
                    <span className="text-[10px] font-semibold text-slate-400 bg-slate-900 px-1.5 py-0.5 rounded border border-slate-800">
                      {item.weight}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-0.5">{item.description}</p>
                </div>
              </div>
              <span className="font-mono font-bold text-sm text-cyan-300">{score.toFixed(1)}%</span>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
              <div
                className={`h-full rounded-full bg-gradient-to-r ${item.color} transition-all duration-700 ease-out`}
                style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};
