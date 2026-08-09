import React, { useState } from 'react';
import { FileText, Search, Upload, Filter, Layers, GitFork } from 'lucide-react';
import { useApp } from '../context/AppContext';
import { PDFUploader } from '../components/DocumentCard/PDFUploader';
import { DocumentCard } from '../components/DocumentCard/DocumentCard';
import { EmptyState } from '../components/EmptyState/EmptyState';

export const Documents = () => {
  const { uploadedDocuments } = useApp();
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDocs = uploadedDocuments.filter((doc) =>
    doc.filename.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-100 tracking-tight flex items-center gap-2">
          <FileText className="w-6 h-6 text-indigo-400" />
          Document Ingestion & Management
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Upload PDF documents to automatically trigger Module 1 text chunking and Module 2 Neo4j entity graph construction.
        </p>
      </div>

      {/* PDF Upload Section */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-4">
        <h3 className="font-bold text-sm text-slate-200 flex items-center gap-2">
          <Upload className="w-4 h-4 text-cyan-400" />
          Upload New Research PDF Document
        </h3>
        <PDFUploader />
      </div>

      {/* Document Library List */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-800 space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
          <div>
            <h3 className="font-bold text-sm text-slate-200">Ingested PDF Knowledge Base</h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Showing {filteredDocs.length} of {uploadedDocuments.length} total documents
            </p>
          </div>

          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search documents by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 w-full sm:w-64"
            />
          </div>
        </div>

        {filteredDocs.length === 0 ? (
          <EmptyState
            title="No PDF documents match search"
            message="Upload a PDF above to ingest it into ChromaDB vector store and Neo4j knowledge graph."
            icon={FileText}
          />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredDocs.map((doc) => (
              <DocumentCard key={doc.id} doc={doc} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
