import React from 'react';
import { Brain, Layers, GitFork, ShieldCheck, Server, Layout, ArrowDown, Code2, BookOpen } from 'lucide-react';

export const About = () => {
  const modules = [
    {
      id: 'Module 1',
      title: 'Document Ingestion',
      icon: Layers,
      color: 'border-indigo-500/40 text-indigo-400 bg-indigo-950/20',
      details: 'PDF parsing, recursive text splitting into 500-char chunks with overlap, metadata extraction.',
    },
    {
      id: 'Module 2',
      title: 'Knowledge Representation',
      icon: GitFork,
      color: 'border-cyan-500/40 text-cyan-400 bg-cyan-950/20',
      details: 'spaCy NLP entity extraction, ChromaDB vector embedding storage, and Neo4j graph triple construction.',
    },
    {
      id: 'Module 3',
      title: 'GraphRAG Retrieval',
      icon: Brain,
      color: 'border-purple-500/40 text-purple-400 bg-purple-950/20',
      details: 'Hybrid dense (SentenceTransformers) + sparse vector search with Neo4j subgraph traversal.',
    },
    {
      id: 'Module 4',
      title: 'LLM + Trust Engine',
      icon: ShieldCheck,
      color: 'border-emerald-500/40 text-emerald-400 bg-emerald-950/20',
      details: 'Ollama Llama 3 answer synthesis, 4-tier Trust Score calculation, and inline citation generation.',
    },
    {
      id: 'Module 5',
      title: 'Backend API Service',
      icon: Server,
      color: 'border-amber-500/40 text-amber-400 bg-amber-950/20',
      details: 'FastAPI server exposing endpoints for /health, /upload, /ask, /graph, /dashboard, and /trust.',
    },
    {
      id: 'Module 6',
      title: 'Frontend Research Dashboard',
      icon: Layout,
      color: 'border-pink-500/40 text-pink-400 bg-pink-950/20',
      details: 'Modern React + Vite + Tailwind CSS dark AI research UI with interactive graph visualizer & RAG chat workspace.',
    },
  ];

  const techStack = [
    { name: 'Python 3.10+', role: 'Core Backend Environment' },
    { name: 'FastAPI', role: 'High-Performance REST API Server' },
    { name: 'ChromaDB', role: 'Persistent Dense Vector Store' },
    { name: 'Neo4j Database', role: 'Graph Database & Cypher Triples' },
    { name: 'spaCy NLP', role: 'Named Entity Recognition (NER)' },
    { name: 'SentenceTransformers', role: 'all-MiniLM-L6-v2 Embeddings' },
    { name: 'Ollama & Llama 3', role: 'Local LLM Inference Engine' },
    { name: 'React 19 & Vite', role: 'Frontend Application Framework' },
    { name: 'Tailwind CSS v4', role: 'Glassmorphic Styling System' },
    { name: 'Recharts & Lucide', role: 'Data Visualization & UI Icons' },
  ];

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="glass-panel p-8 rounded-3xl border border-slate-800 bg-gradient-to-r from-indigo-950/50 via-slate-900/80 to-purple-950/40 text-center space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
          <BookOpen className="w-3.5 h-3.5" />
          EDI Semester 5 Capstone Research Project
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-100 tracking-tight">
          Adaptive Living GraphRAG
        </h1>
        <p className="text-sm text-slate-300 max-w-2xl mx-auto">
          A Trust-Aware Dynamic Knowledge Evolution Framework for Real-Time LLM Retrieval
        </p>
      </div>

      {/* Pipeline Architecture Diagram */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-6">
        <h3 className="font-bold text-base text-slate-200 text-center">
          End-to-End 6-Module Pipeline Architecture
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {modules.map((mod, idx) => {
            const Icon = mod.icon;
            return (
              <div key={mod.id} className={`glass-panel p-4 rounded-2xl border ${mod.color} flex flex-col justify-between space-y-3`}>
                <div className="flex items-center justify-between">
                  <span className="text-[10px] uppercase font-bold tracking-wider opacity-80">{mod.id}</span>
                  <div className="p-2 rounded-xl bg-slate-950 border border-slate-800">
                    <Icon className="w-4 h-4" />
                  </div>
                </div>

                <div>
                  <h4 className="font-bold text-sm text-slate-100">{mod.title}</h4>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">{mod.details}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Tech Stack Grid */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
        <h3 className="font-bold text-base text-slate-200 flex items-center gap-2">
          <Code2 className="w-5 h-5 text-cyan-400" />
          Technology Stack Specification
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          {techStack.map((tech) => (
            <div key={tech.name} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex justify-between items-center">
              <span className="font-bold text-slate-200">{tech.name}</span>
              <span className="text-[11px] text-slate-400">{tech.role}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
