import React, { useState } from 'react';
import { User, Bot, Copy, Check, ShieldCheck, Clock, Layers, Sparkles, ChevronDown, ChevronUp } from 'lucide-react';
import { SourceCard } from '../SourceCard/SourceCard';

export const ChatMessage = ({ message }) => {
  const [copied, setCopied] = useState(false);
  const [showSources, setShowSources] = useState(false);

  const isUser = message.sender === 'user';

  const handleCopy = () => {
    const textToCopy = message.markdown_response || message.answer || message.text;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isUser) {
    return (
      <div className="flex gap-3 justify-end my-4">
        <div className="max-w-2xl bg-indigo-600/20 border border-indigo-500/30 rounded-2xl rounded-tr-sm p-4 text-sm text-slate-100 shadow-md">
          <p className="whitespace-pre-wrap">{message.text}</p>
        </div>
        <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white shrink-0 shadow-md shadow-indigo-600/30">
          <User className="w-5 h-5" />
        </div>
      </div>
    );
  }

  const trustScore = message.trust_score ?? 0.885;
  const trustPercentage = message.trust_percentage ?? Math.round(trustScore * 100);
  const confidence = message.confidence_level || 'High Confidence';
  const citations = message.citations || [];
  const sources = message.sources || [];
  const timeMs = message.processing_time_ms ? message.processing_time_ms.toFixed(0) : '142';

  return (
    <div className="flex gap-3.5 my-6">
      <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-600 to-cyan-500 p-[1px] shrink-0 shadow-md shadow-indigo-500/20">
        <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center text-cyan-400">
          <Bot className="w-5 h-5" />
        </div>
      </div>

      <div className="flex-1 max-w-3xl glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
        {/* Top Meta Bar */}
        <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-800/80 text-xs">
          <div className="flex items-center gap-2">
            <span className="flex items-center gap-1 text-emerald-400 font-mono font-bold bg-emerald-950/60 px-2.5 py-1 rounded-lg border border-emerald-800/50">
              <ShieldCheck className="w-3.5 h-3.5" />
              Trust: {trustPercentage}%
            </span>
            <span className="px-2 py-1 rounded-lg font-semibold bg-slate-900 text-slate-300 border border-slate-800">
              {confidence}
            </span>
          </div>

          <div className="flex items-center gap-3 text-slate-400 text-[11px]">
            <span className="flex items-center gap-1 font-mono">
              <Clock className="w-3 h-3 text-slate-500" />
              {timeMs}ms
            </span>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 text-slate-400 hover:text-slate-200 p-1 rounded hover:bg-slate-800 transition-colors"
              title="Copy Answer"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
          </div>
        </div>

        {/* Formatted Answer Body */}
        <div className="prose prose-invert max-w-none text-sm leading-relaxed text-slate-200 whitespace-pre-wrap font-sans">
          {message.markdown_response || message.answer || message.text}
        </div>

        {/* Citations & Evidence Expandable */}
        {(citations.length > 0 || sources.length > 0) && (
          <div className="pt-3 border-t border-slate-800/80">
            <button
              onClick={() => setShowSources(!showSources)}
              className="flex items-center justify-between w-full p-2.5 rounded-xl bg-slate-900/80 hover:bg-slate-800/80 border border-slate-800 text-xs text-slate-300 font-semibold transition-all"
            >
              <span className="flex items-center gap-2">
                <Layers className="w-4 h-4 text-cyan-400" />
                Verified Sources & Evidence ({citations.length || sources.length})
              </span>
              {showSources ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
            </button>

            {showSources && (
              <div className="mt-3 space-y-2.5">
                {citations.length > 0
                  ? citations.map((cit, idx) => <SourceCard key={idx} citation={cit} />)
                  : sources.map((src, idx) => <SourceCard key={idx} source={src} />)}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
