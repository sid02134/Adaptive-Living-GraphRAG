import React, { useState, useEffect } from 'react';
import {
  GitMerge,
  ShieldCheck,
  Clock,
  Sparkles,
  AlertTriangle,
  RefreshCw,
  PlusCircle,
  Search,
  CheckCircle2,
  XCircle,
  Archive,
  ArrowRight,
  Sliders,
  Layers,
  Activity,
} from 'lucide-react';
import { evolutionService } from '../services/evolutionService';

export const KnowledgeEvolution = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(false);
  const [statusData, setStatusData] = useState(null);
  const [historyData, setHistoryData] = useState([]);
  const [conflictsData, setConflictsData] = useState([]);

  // Form State for Knowledge Evolution Update
  const [updateForm, setUpdateForm] = useState({
    subject: '',
    predicate: '',
    object: '',
    source: 'user_input',
    source_type: 'official_doc',
    confidence: 0.85,
    context_chunk: '',
  });
  const [updateResult, setUpdateResult] = useState(null);

  // State for Adaptive Retrieval Playground
  const [retrievalQuery, setRetrievalQuery] = useState('');
  const [weights, setWeights] = useState({
    vector_weight: 0.35,
    graph_weight: 0.25,
    trust_weight: 0.20,
    freshness_weight: 0.20,
  });
  const [includeHistorical, setIncludeHistorical] = useState(false);
  const [retrievalResults, setRetrievalResults] = useState(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [statusRes, historyRes, conflictsRes] = await Promise.all([
        evolutionService.getStatus().catch(() => null),
        evolutionService.getHistory(30).catch(() => ({ history: [] })),
        evolutionService.getConflicts().catch(() => ({ conflicts: [] })),
      ]);

      if (statusRes) setStatusData(statusRes);
      if (historyRes?.history) setHistoryData(historyRes.history);
      if (conflictsRes?.conflicts) setConflictsData(conflictsRes.conflicts);
    } catch (err) {
      console.error('Failed to fetch evolution data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleUpdateSubmit = async (e) => {
    e.preventDefault();
    if (!updateForm.subject || !updateForm.predicate || !updateForm.object) return;
    setLoading(true);
    try {
      const res = await evolutionService.updateKnowledge(updateForm);
      if (res?.evolution_result) {
        setUpdateResult(res.evolution_result);
        fetchDashboardData();
      }
    } catch (err) {
      alert('Error updating knowledge: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleConflictResolve = async (conflictId, winningClaimId) => {
    setLoading(true);
    try {
      await evolutionService.resolveConflictFeedback(conflictId, winningClaimId, 'Manual override via UI');
      fetchDashboardData();
    } catch (err) {
      alert('Error resolving conflict: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleAdaptiveQuery = async (e) => {
    e.preventDefault();
    if (!retrievalQuery) return;
    setLoading(true);
    try {
      const res = await evolutionService.adaptiveQuery({
        query: retrievalQuery,
        top_k: 5,
        include_historical: includeHistorical,
        ...weights,
      });
      if (res?.adaptive_retrieval) {
        setRetrievalResults(res.adaptive_retrieval);
      }
    } catch (err) {
      alert('Error performing adaptive retrieval: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const getDecisionBadge = (decision) => {
    switch (decision) {
      case 'ADD':
        return <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 flex items-center gap-1"><PlusCircle className="w-3.5 h-3.5" /> ADD</span>;
      case 'UPDATE':
        return <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 flex items-center gap-1"><RefreshCw className="w-3.5 h-3.5" /> UPDATE</span>;
      case 'REPLACE':
        return <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30 flex items-center gap-1"><GitMerge className="w-3.5 h-3.5" /> REPLACE</span>;
      case 'ARCHIVE':
        return <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/30 flex items-center gap-1"><Archive className="w-3.5 h-3.5" /> ARCHIVE</span>;
      default:
        return <span className="px-2.5 py-1 rounded-md text-xs font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 flex items-center gap-1"><XCircle className="w-3.5 h-3.5" /> REJECT</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-slate-900/90 via-indigo-950/40 to-slate-900/90 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-500 p-[1px] shadow-lg shadow-cyan-500/20">
            <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center">
              <GitMerge className="w-6 h-6 text-cyan-400" />
            </div>
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
              Module 6: Dynamic Knowledge Evolution
              <span className="text-xs px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-mono">
                Active Engine
              </span>
            </h1>
            <p className="text-sm text-slate-400 mt-0.5">
              5-Factor Adaptive Knowledge Graph Evolution, Conflict Resolution & Temporal Aging
            </p>
          </div>
        </div>
        <button
          onClick={fetchDashboardData}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-sm font-semibold transition border border-slate-700"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /> Refresh Status
        </button>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2">
        {[
          { id: 'overview', label: 'Engine Overview', icon: Layers },
          { id: 'evolve', label: 'Evolve Knowledge', icon: PlusCircle },
          { id: 'conflicts', label: `Conflict Center (${conflictsData.length})`, icon: AlertTriangle },
          { id: 'retrieval', label: '4-Factor Adaptive Retrieval', icon: Sliders },
          { id: 'history', label: 'Audit History', icon: Clock },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-3 font-semibold text-sm transition-all rounded-t-xl border-b-2 ${
                activeTab === tab.id
                  ? 'border-cyan-400 text-cyan-400 bg-slate-900/60'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" /> {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab 1: Overview */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {[
              { title: 'ADD Decisions', count: statusData?.decisions_summary?.ADD || 0, color: 'text-emerald-400', bg: 'from-emerald-950/30' },
              { title: 'UPDATE Decisions', count: statusData?.decisions_summary?.UPDATE || 0, color: 'text-cyan-400', bg: 'from-cyan-950/30' },
              { title: 'REPLACE Decisions', count: statusData?.decisions_summary?.REPLACE || 0, color: 'text-amber-400', bg: 'from-amber-950/30' },
              { title: 'ARCHIVE Decisions', count: statusData?.decisions_summary?.ARCHIVE || 0, color: 'text-purple-400', bg: 'from-purple-950/30' },
              { title: 'Active Conflicts', count: conflictsData.filter(c => c.resolution_status === 'UNRESOLVED').length, color: 'text-rose-400', bg: 'from-rose-950/30' },
            ].map((card, i) => (
              <div key={i} className={`p-4 rounded-xl border border-slate-800 bg-gradient-to-b ${card.bg} to-slate-900/80`}>
                <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">{card.title}</span>
                <p className={`text-2xl font-bold ${card.color} mt-1 font-mono`}>{card.count}</p>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
              <h2 className="text-base font-bold text-slate-200 flex items-center gap-2">
                <Activity className="w-5 h-5 text-cyan-400" /> Module 6 Functional Engines
              </h2>
              <ul className="space-y-3">
                {[
                  { name: '1. Adaptive Knowledge Evolution Engine', desc: 'Evaluates facts & emits ADD / UPDATE / REPLACE / ARCHIVE / REJECT decisions.' },
                  { name: '2. Conflict Resolution Engine', desc: 'Detects contradictions & enforces configurable resolution policies.' },
                  { name: '3. Trust & Confidence Engine', desc: 'Calculates multi-factor score: S_rel, S_fresh, S_evid, S_agree, S_relv.' },
                  { name: '4. Temporal Knowledge Aging Engine', desc: 'Computes exponential time decay (Freshness = exp(-lambda*t)) & validity flags.' },
                  { name: '5. Adaptive Retrieval Engine', desc: 'Combines Vector (w1) + Graph (w2) + Trust (w3) + Freshness (w4) scores.' },
                ].map((e, idx) => (
                  <li key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                    <h3 className="text-sm font-bold text-slate-200">{e.name}</h3>
                    <p className="text-xs text-slate-400 mt-0.5">{e.desc}</p>
                  </li>
                ))}
              </ul>
            </div>

            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
              <h2 className="text-base font-bold text-slate-200 flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-indigo-400" /> Engine Parameters & Config
              </h2>
              <div className="space-y-3 font-mono text-xs">
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                  <span className="text-slate-400">Default Conflict Policy:</span>
                  <span className="text-cyan-300 font-bold">{statusData?.configuration?.default_conflict_policy || 'WEIGHTED_HYBRID'}</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                  <span className="text-slate-400">Lambda Decay Constant (λ):</span>
                  <span className="text-emerald-300 font-bold">{statusData?.configuration?.lambda_decay || 0.01}</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                  <span className="text-slate-400">Outdated Threshold (Days):</span>
                  <span className="text-amber-300 font-bold">{statusData?.configuration?.outdated_threshold_days || 180} days</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center">
                  <span className="text-slate-400">Archive Threshold (Days):</span>
                  <span className="text-purple-300 font-bold">{statusData?.configuration?.archive_threshold_days || 365} days</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Evolve Knowledge */}
      {activeTab === 'evolve' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <form onSubmit={handleUpdateSubmit} className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h2 className="text-base font-bold text-slate-200 flex items-center gap-2">
              <PlusCircle className="w-5 h-5 text-cyan-400" /> Submit Fact Triple for Evolution
            </h2>

            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="text-xs font-semibold text-slate-400">Subject Entity</label>
                <input
                  type="text"
                  placeholder="e.g. Sam Altman"
                  value={updateForm.subject}
                  onChange={(e) => setUpdateForm({ ...updateForm, subject: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:border-cyan-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-400">Predicate</label>
                <input
                  type="text"
                  placeholder="e.g. is_CEO_of"
                  value={updateForm.predicate}
                  onChange={(e) => setUpdateForm({ ...updateForm, predicate: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:border-cyan-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-400">Object Entity</label>
                <input
                  type="text"
                  placeholder="e.g. OpenAI"
                  value={updateForm.object}
                  onChange={(e) => setUpdateForm({ ...updateForm, object: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:border-cyan-500 outline-none"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs font-semibold text-slate-400">Source Document / Origin</label>
                <input
                  type="text"
                  value={updateForm.source}
                  onChange={(e) => setUpdateForm({ ...updateForm, source: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 outline-none"
                />
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-400">Source Reliability Type</label>
                <select
                  value={updateForm.source_type}
                  onChange={(e) => setUpdateForm({ ...updateForm, source_type: e.target.value })}
                  className="w-full mt-1 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 outline-none"
                >
                  <option value="peer_reviewed_journal">Peer Reviewed Journal (0.95)</option>
                  <option value="official_doc">Official Document (0.90)</option>
                  <option value="verified_database">Verified Database (0.85)</option>
                  <option value="news_article">News Article (0.70)</option>
                  <option value="user_input">User Input (0.60)</option>
                  <option value="blog_post">Blog Post (0.50)</option>
                </select>
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-400">Context Supporting Text Chunk</label>
              <textarea
                rows={3}
                placeholder="Optional text chunk providing contextual evidence for this claim..."
                value={updateForm.context_chunk}
                onChange={(e) => setUpdateForm({ ...updateForm, context_chunk: e.target.value })}
                className="w-full mt-1 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white rounded-xl font-bold text-sm shadow-lg shadow-indigo-500/20"
            >
              {loading ? 'Evaluating Evolution...' : 'Evaluate & Update Knowledge Graph'}
            </button>
          </form>

          {/* Result Card */}
          <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h2 className="text-base font-bold text-slate-200 flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-indigo-400" /> Evaluation Output Result
            </h2>
            {updateResult ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-xs font-semibold text-slate-400">Decision Outcome:</span>
                  {getDecisionBadge(updateResult.decision)}
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-xs font-semibold text-slate-400 block mb-1">Reasoning:</span>
                  <p className="text-xs text-slate-200 leading-relaxed">{updateResult.reasoning}</p>
                </div>
                {updateResult.trust_breakdown && (
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-slate-400">System Trust Score:</span>
                      <span className="font-bold text-cyan-400">{updateResult.trust_breakdown.score_percentage || updateResult.trust_breakdown.overall_trust_score}</span>
                    </div>
                    <p className="text-[11px] text-slate-400 italic">{updateResult.trust_breakdown.interpretation}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="p-12 text-center text-slate-500 text-xs italic border border-dashed border-slate-800 rounded-xl">
                Submit a fact triple to see real-time evolution decision, trust evaluation, and incremental update output.
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tab 3: Conflict Center */}
      {activeTab === 'conflicts' && (
        <div className="space-y-4">
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400" />
            <span>
              Contradiction detection identifies competing claims (same Subject + Predicate with differing Objects).
              Apply resolution policies or manual overrides below.
            </span>
          </div>

          {conflictsData.length === 0 ? (
            <div className="p-12 text-center text-slate-500 text-xs border border-slate-800 rounded-2xl bg-slate-900/60">
              No conflicting knowledge claims currently detected in the system.
            </div>
          ) : (
            <div className="space-y-4">
              {conflictsData.map((conflict, i) => (
                <div key={i} className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-cyan-400">{conflict.conflict_id}</span>
                    <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold ${conflict.resolution_status.startsWith('RESOLVED') ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}`}>
                      {conflict.resolution_status}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-[11px] font-semibold text-slate-400">Claim A (Existing)</span>
                      <p className="text-xs font-mono text-slate-200 mt-1">
                        {conflict.claim_a?.subject} {conflict.claim_a?.predicate} <strong className="text-amber-400">{conflict.claim_a?.object}</strong>
                      </p>
                      <span className="text-[10px] text-slate-500 mt-1 block">Source: {conflict.claim_a?.source} | Timestamp: {conflict.claim_a?.timestamp}</span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <span className="text-[11px] font-semibold text-slate-400">Claim B (Incoming)</span>
                      <p className="text-xs font-mono text-slate-200 mt-1">
                        {conflict.claim_b?.subject} {conflict.claim_b?.predicate} <strong className="text-cyan-400">{conflict.claim_b?.object}</strong>
                      </p>
                      <span className="text-[10px] text-slate-500 mt-1 block">Source: {conflict.claim_b?.source} | Timestamp: {conflict.claim_b?.timestamp}</span>
                    </div>
                  </div>

                  {conflict.resolution_status === 'UNRESOLVED' && (
                    <div className="flex gap-2 pt-2">
                      <button
                        onClick={() => handleConflictResolve(conflict.conflict_id, conflict.claim_a?.id)}
                        className="px-3 py-1.5 bg-amber-600/30 hover:bg-amber-600/50 text-amber-200 rounded-lg text-xs font-semibold border border-amber-500/30"
                      >
                        Keep Claim A
                      </button>
                      <button
                        onClick={() => handleConflictResolve(conflict.conflict_id, conflict.claim_b?.id)}
                        className="px-3 py-1.5 bg-cyan-600/30 hover:bg-cyan-600/50 text-cyan-200 rounded-lg text-xs font-semibold border border-cyan-500/30"
                      >
                        Accept Claim B (Replace)
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tab 4: 4-Factor Adaptive Retrieval */}
      {activeTab === 'retrieval' && (
        <div className="space-y-6">
          <form onSubmit={handleAdaptiveQuery} className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h2 className="text-base font-bold text-slate-200 flex items-center gap-2">
              <Sliders className="w-5 h-5 text-cyan-400" /> 4-Factor Adaptive Retrieval Configuration
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-xs">
              <div>
                <label className="text-slate-400 font-semibold block mb-1">Vector Weight: {weights.vector_weight}</label>
                <input
                  type="range" min="0" max="1" step="0.05"
                  value={weights.vector_weight}
                  onChange={(e) => setWeights({ ...weights, vector_weight: parseFloat(e.target.value) })}
                  className="w-full accent-cyan-400"
                />
              </div>
              <div>
                <label className="text-slate-400 font-semibold block mb-1">Graph Weight: {weights.graph_weight}</label>
                <input
                  type="range" min="0" max="1" step="0.05"
                  value={weights.graph_weight}
                  onChange={(e) => setWeights({ ...weights, graph_weight: parseFloat(e.target.value) })}
                  className="w-full accent-indigo-400"
                />
              </div>
              <div>
                <label className="text-slate-400 font-semibold block mb-1">Trust Weight: {weights.trust_weight}</label>
                <input
                  type="range" min="0" max="1" step="0.05"
                  value={weights.trust_weight}
                  onChange={(e) => setWeights({ ...weights, trust_weight: parseFloat(e.target.value) })}
                  className="w-full accent-emerald-400"
                />
              </div>
              <div>
                <label className="text-slate-400 font-semibold block mb-1">Freshness Weight: {weights.freshness_weight}</label>
                <input
                  type="range" min="0" max="1" step="0.05"
                  value={weights.freshness_weight}
                  onChange={(e) => setWeights({ ...weights, freshness_weight: parseFloat(e.target.value) })}
                  className="w-full accent-amber-400"
                />
              </div>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="hist"
                checked={includeHistorical}
                onChange={(e) => setIncludeHistorical(e.target.checked)}
                className="w-4 h-4 rounded border-slate-800 text-cyan-500"
              />
              <label htmlFor="hist" className="text-xs text-slate-300 font-semibold">Include Superceded / Archived Historical Knowledge</label>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Enter query string for 4-factor adaptive retrieval..."
                value={retrievalQuery}
                onChange={(e) => setRetrievalQuery(e.target.value)}
                className="flex-1 p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 outline-none focus:border-cyan-500"
                required
              />
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-cyan-500/20 flex items-center gap-2"
              >
                <Search className="w-4 h-4" /> Adaptive Query
              </button>
            </div>
          </form>

          {retrievalResults && (
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-slate-200">Adaptive Retrieval Results ({retrievalResults.results?.length || 0} Ranked Items)</h3>
              <div className="space-y-3">
                {retrievalResults.results?.map((res, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-semibold text-slate-200">{res.id || `Result Chunk #${idx + 1}`}</span>
                      <span className="font-bold text-cyan-400 font-mono">Final Score: {res.final_adaptive_score}</span>
                    </div>
                    <p className="text-xs text-slate-400">{res.document}</p>
                    <div className="flex gap-4 text-[10px] text-slate-500 font-mono pt-1 border-t border-slate-800/80">
                      <span>Vector: {res.vector_score}</span>
                      <span>Graph: {res.graph_score}</span>
                      <span>Trust: {res.trust_score}</span>
                      <span>Freshness: {res.freshness_score}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 5: Audit History */}
      {activeTab === 'history' && (
        <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
          <h2 className="text-base font-bold text-slate-200 flex items-center gap-2">
            <Clock className="w-5 h-5 text-cyan-400" /> Knowledge Evolution Audit Log History
          </h2>
          {historyData.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500">No evolution audit records logged yet.</div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-300 font-mono">
                <thead className="bg-slate-950 text-slate-400 uppercase text-[10px]">
                  <tr>
                    <th className="p-3">Claim ID</th>
                    <th className="p-3">Decision</th>
                    <th className="p-3">Reasoning</th>
                    <th className="p-3">Trust Score</th>
                    <th className="p-3">Timestamp</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {historyData.map((h, i) => (
                    <tr key={i} className="hover:bg-slate-800/40">
                      <td className="p-3 text-cyan-400">{h.claim_id}</td>
                      <td className="p-3">{getDecisionBadge(h.decision)}</td>
                      <td className="p-3 text-slate-300 max-w-xs truncate">{h.reasoning}</td>
                      <td className="p-3 text-emerald-400">{h.trust_breakdown?.score_percentage || '85.0%'}</td>
                      <td className="p-3 text-slate-500">{h.timestamp}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
