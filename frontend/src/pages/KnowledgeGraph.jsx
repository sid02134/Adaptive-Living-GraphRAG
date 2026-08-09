import React, { useState, useEffect } from 'react';
import { Network, GitFork, GitPullRequest, Search, RefreshCw } from 'lucide-react';
import { getKnowledgeGraph } from '../services/graphService';
import { GraphViewer } from '../components/GraphViewer/GraphViewer';
import { SkeletonLoader } from '../components/Loading/SkeletonLoader';
import { ErrorCard } from '../components/ErrorState/ErrorCard';

export const KnowledgeGraph = () => {
  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [queryEntity, setQueryEntity] = useState('');

  const fetchGraph = async (entity = '') => {
    setLoading(true);
    setError(null);
    try {
      const data = await getKnowledgeGraph(entity);
      setGraphData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchGraph(queryEntity);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold text-slate-100 tracking-tight flex items-center gap-2">
            <Network className="w-6 h-6 text-cyan-400" />
            Neo4j Knowledge Graph Visualizer
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Explore extracted entity nodes and semantic relationships generated in Module 2.
          </p>
        </div>

        <button
          onClick={() => fetchGraph(queryEntity)}
          className="p-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-slate-100 text-xs flex items-center gap-1.5 self-start sm:self-auto transition-colors"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-cyan-400' : ''}`} />
          <span>Reload Graph</span>
        </button>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <GitFork className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-semibold text-slate-400">Total Graph Nodes</span>
            <p className="text-xl font-extrabold text-slate-100 font-mono">
              {graphData?.total_nodes ?? '—'}
            </p>
          </div>
        </div>

        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
            <GitPullRequest className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-semibold text-slate-400 font-sans">Total Edge Triples</span>
            <p className="text-xl font-extrabold text-slate-100 font-mono">
              {graphData?.total_edges ?? '—'}
            </p>
          </div>
        </div>

        <form onSubmit={handleSearchSubmit} className="flex items-center">
          <div className="relative w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Filter subgraph entity..."
              value={queryEntity}
              onChange={(e) => setQueryEntity(e.target.value)}
              className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-20 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
            <button
              type="submit"
              className="absolute right-2 top-1.5 px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs rounded-lg transition-colors"
            >
              Search
            </button>
          </div>
        </form>
      </div>

      {/* Main Graph Renderer */}
      {loading ? (
        <SkeletonLoader count={1} />
      ) : error ? (
        <ErrorCard title="Failed to load Neo4j Graph" message={error} onRetry={() => fetchGraph(queryEntity)} />
      ) : (
        <GraphViewer data={graphData} />
      )}
    </div>
  );
};
