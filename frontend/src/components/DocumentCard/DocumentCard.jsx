import React from 'react';
import { FileText, Layers, GitFork, Clock, CheckCircle2 } from 'lucide-react';

export const DocumentCard = ({ doc }) => {
  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800/80 hover:border-slate-700 transition-all flex flex-col justify-between">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <div className="p-2.5 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <h4 className="font-bold text-sm text-slate-200 truncate max-w-[200px] sm:max-w-[280px]">
              {doc.filename}
            </h4>
            <p className="text-[11px] text-slate-400 mt-0.5 flex items-center gap-1">
              <Clock className="w-3 h-3 text-slate-500" />
              Uploaded {new Date(doc.upload_date).toLocaleDateString()}
            </p>
          </div>
        </div>

        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
          <CheckCircle2 className="w-3 h-3" />
          {doc.status || 'Indexed'}
        </span>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800/80 grid grid-cols-2 gap-2 text-xs">
        <div className="flex items-center gap-2 text-slate-400">
          <Layers className="w-4 h-4 text-cyan-400" />
          <span>Chunks: <strong className="text-slate-200 font-mono">{doc.chunks_processed || '—'}</strong></span>
        </div>
        <div className="flex items-center gap-2 text-slate-400">
          <GitFork className="w-4 h-4 text-purple-400" />
          <span>Entities: <strong className="text-slate-200 font-mono">{doc.entities_extracted || '—'}</strong></span>
        </div>
      </div>
    </div>
  );
};
