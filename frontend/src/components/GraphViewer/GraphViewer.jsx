import React, { useState, useEffect, useRef } from 'react';
import { Search, ZoomIn, ZoomOut, RotateCcw, Maximize2, Minimize2, Filter, Info, Tag, Network } from 'lucide-react';

export const GraphViewer = ({ data, onNodeSelect }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [zoomLevel, setZoomLevel] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [isFullscreen, setIsFullscreen] = useState(false);

  const containerRef = useRef(null);

  useEffect(() => {
    if (!data?.nodes) return;

    // Calculate node positions in a nice circular/radial layout for visualization
    const rawNodes = data.nodes || [];
    const rawEdges = data.edges || [];
    const count = rawNodes.length;

    const width = 800;
    const height = 500;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.35;

    const positionedNodes = rawNodes.map((n, idx) => {
      const angle = (idx / count) * 2 * Math.PI;
      const x = centerX + radius * Math.cos(angle) + (Math.random() - 0.5) * 40;
      const y = centerY + radius * Math.sin(angle) + (Math.random() - 0.5) * 40;
      return {
        ...n,
        x,
        y,
        category: n.label || 'Entity',
      };
    });

    setNodes(positionedNodes);
    setEdges(rawEdges);
  }, [data]);

  // Categories list
  const categories = ['ALL', ...new Set((data?.nodes || []).map((n) => n.label || 'Entity'))];

  // Filtering
  const filteredNodes = nodes.filter((n) => {
    const matchesSearch = n.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'ALL' || n.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const filteredNodeIds = new Set(filteredNodes.map((n) => n.id));
  const filteredEdges = edges.filter(
    (e) => filteredNodeIds.has(e.source) && filteredNodeIds.has(e.target)
  );

  const handleNodeClick = (node) => {
    setSelectedNode(node);
    if (onNodeSelect) onNodeSelect(node);
  };

  const handleMouseDown = (e) => {
    if (e.target.tagName === 'svg' || e.target.tagName === 'g') {
      setIsDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isDragging) {
      setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const resetView = () => {
    setZoomLevel(1);
    setPan({ x: 0, y: 0 });
    setSelectedNode(null);
    setSearchQuery('');
    setSelectedCategory('ALL');
  };

  const getNodeColor = (label) => {
    switch (label?.toUpperCase()) {
      case 'CONCEPT':
        return { bg: '#818CF8', border: '#6366F1' };
      case 'DATABASE':
        return { bg: '#38BDF8', border: '#0284C7' };
      case 'MODEL':
        return { bg: '#C084FC', border: '#9333EA' };
      case 'MODULE':
        return { bg: '#34D399', border: '#059669' };
      default:
        return { bg: '#F472B6', border: '#DB2777' };
    }
  };

  return (
    <div
      ref={containerRef}
      className={`glass-panel rounded-2xl overflow-hidden border border-slate-800 flex flex-col relative transition-all ${
        isFullscreen ? 'fixed inset-0 z-50 rounded-none bg-[#080C14]' : 'h-[600px]'
      }`}
    >
      {/* Top Toolbar */}
      <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 z-10">
        <div className="flex items-center gap-2">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search graph entities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div className="flex items-center gap-1">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center gap-1.5 text-xs">
          <button
            onClick={() => setZoomLevel((z) => Math.min(z + 0.2, 2.5))}
            className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:bg-slate-800"
            title="Zoom In"
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <button
            onClick={() => setZoomLevel((z) => Math.max(z - 0.2, 0.4))}
            className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:bg-slate-800"
            title="Zoom Out"
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={resetView}
            className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:bg-slate-800"
            title="Reset View"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 hover:bg-slate-800"
            title="Toggle Fullscreen"
          >
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {/* SVG Canvas Area */}
      <div
        className="flex-1 relative cursor-grab active:cursor-grabbing overflow-hidden bg-[#070A12]"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
      >
        <svg
          width="100%"
          height="100%"
          viewBox="0 0 800 500"
          className="w-full h-full select-none"
        >
          <g transform={`translate(${pan.x}, ${pan.y}) scale(${zoomLevel})`}>
            {/* Draw Edges */}
            {filteredEdges.map((edge, idx) => {
              const sourceNode = nodes.find((n) => n.id === edge.source);
              const targetNode = nodes.find((n) => n.id === edge.target);

              if (!sourceNode || !targetNode) return null;

              const midX = (sourceNode.x + targetNode.x) / 2;
              const midY = (sourceNode.y + targetNode.y) / 2;

              return (
                <g key={idx}>
                  <line
                    x1={sourceNode.x}
                    y1={sourceNode.y}
                    x2={targetNode.x}
                    y2={targetNode.y}
                    stroke="rgba(99, 102, 241, 0.4)"
                    strokeWidth="1.5"
                    strokeDasharray="4 2"
                  />
                  <text
                    x={midX}
                    y={midY}
                    fill="#94A3B8"
                    fontSize="9"
                    fontFamily="monospace"
                    textAnchor="middle"
                    className="bg-slate-950 px-1 py-0.5 rounded pointer-events-none"
                  >
                    {edge.relationship}
                  </text>
                </g>
              );
            })}

            {/* Draw Nodes */}
            {filteredNodes.map((node) => {
              const isSelected = selectedNode?.id === node.id;
              const style = getNodeColor(node.category);

              return (
                <g
                  key={node.id}
                  transform={`translate(${node.x}, ${node.y})`}
                  onClick={(e) => {
                    e.stopPropagation();
                    handleNodeClick(node);
                  }}
                  className="cursor-pointer group"
                >
                  <circle
                    r={isSelected ? 22 : 18}
                    fill={style.bg}
                    stroke={isSelected ? '#38BDF8' : style.border}
                    strokeWidth={isSelected ? 3 : 2}
                    className="transition-all duration-300 drop-shadow-md group-hover:scale-110"
                  />
                  <text
                    y={28}
                    textAnchor="middle"
                    fill="#E2E8F0"
                    fontSize="11"
                    fontWeight="600"
                    fontFamily="sans-serif"
                    className="pointer-events-none drop-shadow-sm"
                  >
                    {node.id}
                  </text>
                  <text
                    y={40}
                    textAnchor="middle"
                    fill="#94A3B8"
                    fontSize="9"
                    fontFamily="monospace"
                    className="pointer-events-none"
                  >
                    [{node.category}]
                  </text>
                </g>
              );
            })}
          </g>
        </svg>

        {/* Selected Node Drawer */}
        {selectedNode && (
          <div className="absolute right-4 top-4 w-72 glass-panel p-4 rounded-xl border border-slate-800 z-20 text-xs shadow-2xl animate-in fade-in slide-in-from-right-5">
            <div className="flex items-center justify-between pb-2 border-b border-slate-800">
              <span className="font-bold text-slate-200 flex items-center gap-1.5">
                <Network className="w-4 h-4 text-cyan-400" />
                Entity Details
              </span>
              <button
                onClick={() => setSelectedNode(null)}
                className="text-slate-400 hover:text-slate-200 font-bold"
              >
                ✕
              </button>
            </div>

            <div className="mt-3 space-y-2">
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-semibold">Entity ID</span>
                <p className="font-bold text-sm text-cyan-300 font-mono">{selectedNode.id}</p>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-semibold">Label Category</span>
                <p className="font-semibold text-slate-200 mt-0.5">
                  <span className="px-2 py-0.5 rounded bg-indigo-950 text-indigo-300 border border-indigo-800">
                    {selectedNode.category}
                  </span>
                </p>
              </div>

              <div>
                <span className="text-[10px] text-slate-500 uppercase font-semibold">Connected Relationships</span>
                <div className="mt-1 space-y-1 max-h-32 overflow-y-auto">
                  {edges
                    .filter((e) => e.source === selectedNode.id || e.target === selectedNode.id)
                    .map((e, idx) => (
                      <div
                        key={idx}
                        className="p-1.5 rounded bg-slate-900 border border-slate-800 text-[11px] font-mono text-slate-300"
                      >
                        {e.source} ➔ <strong className="text-cyan-400">{e.relationship}</strong> ➔ {e.target}
                      </div>
                    ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
