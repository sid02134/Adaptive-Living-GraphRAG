import React, { useState } from 'react';
import { FileText, ExternalLink, ChevronDown, ChevronUp, Tag, Layers } from 'lucide-react';

export const SourceCard = ({ citation, source }) => {
  const [expanded, setExpanded] = useState(false);

  const citationId = citation?.citation_id || source?.citation_id || '[Ref]';
  const sourceFile = citation?.source_file || source?.source_file || source?.filename || 'Document.pdf';
  const chunkId = citation?.chunk_id || source?.chunk_id || 'chunk_001';
  const score = citation?.relevance_score ?? source?.score ?? source?.relevance_score ?? 0.85;
  const content = source?.chunk_text || source?.content || citation?.formatted_citation || 'Retrieved context chunk text placeholder.';

  const relevancePercentage = Math.round(score > 1 ? score : score * 100);

  return (
    <div className="glass-panel rounded-xl p-3.5 border border-slate-800/80 hover:border-slate-700 transition-all text-xs">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="px-2 py-0.5 rounded font-mono font-bold text-[11px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
            {citationId}
          </span>
          <span className="font-semibold text-slate-200 truncate flex items-center gap-1">
            <FileText className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
            {sourceFile}
          </span>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <span className="font-mono text-[11px] font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/50">
            {relevancePercentage}% Match
          </span>
          <button
            onClick={() => setExpanded(!expanded)}
            className="p-1 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      <div className="mt-2 flex items-center gap-3 text-[11px] text-slate-400">
        <span className="flex items-center gap-1 font-mono">
          <Layers className="w-3 h-3 text-purple-400" />
          Chunk: {chunkId}
        </span>
      </div>

      {expanded && (
        <div className="mt-3 pt-3 border-t border-slate-800/80 bg-slate-950/60 p-3 rounded-lg text-slate-300 font-mono text-[11px] leading-relaxed whitespace-pre-wrap">
          {content}
        </div>
      )}
    </div>
  );
};
