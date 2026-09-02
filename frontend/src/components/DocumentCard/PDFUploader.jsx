import React, { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { uploadDocument } from '../../services/documentService';
import { useApp } from '../../context/AppContext';

export const PDFUploader = ({ onUploadSuccess }) => {
  const { addDocument, refreshHealth } = useApp();
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [statusMessage, setStatusMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = async (file) => {
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {

      setErrorMessage('Invalid file format. Only PDF files are supported.');
      return;
    }

    setLoading(true);
    setProgress(0);
    setStatusMessage('Uploading PDF and building knowledge graph...');
    setErrorMessage(null);

    try {
      const response = await uploadDocument(file, (percent) => {
        setProgress(percent);
      });

      setStatusMessage(
        `Successfully ingested '${response.filename}'. Created ${response.chunks_processed} chunks & extracted ${response.entities_extracted} graph entities.`
      );
      
      // Update global document context
      addDocument(response);
      refreshHealth();

      if (onUploadSuccess) {
        onUploadSuccess(response);
      }
    } catch (err) {
      setErrorMessage(err.message || 'PDF ingestion failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  return (
    <div className="space-y-4">
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !loading && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300 ${
          isDragging
            ? 'border-cyan-400 bg-cyan-950/20 shadow-lg shadow-cyan-500/10'
            : 'border-slate-800 hover:border-slate-700 bg-slate-900/40 hover:bg-slate-900/60'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
            {loading ? (
              <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
            ) : (
              <Upload className="w-8 h-8 text-cyan-400" />
            )}
          </div>

          <div>
            <h3 className="font-bold text-base text-slate-200">
              {loading ? 'Processing Document...' : 'Drag & drop PDF document here'}
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Automated Module 1 text chunking & Module 2 Neo4j entity extraction
            </p>
          </div>

          {!loading && (
            <button
              type="button"
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-600 hover:from-indigo-500 hover:to-cyan-500 text-white font-semibold text-xs shadow-md shadow-indigo-500/20"
            >
              Browse PDF File
            </button>
          )}

          {loading && (
            <div className="w-full max-w-xs mt-2">
              <div className="flex justify-between text-xs text-slate-400 mb-1">
                <span>Ingestion Pipeline</span>
                <span>{progress}%</span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div
                  className="bg-gradient-to-r from-indigo-500 to-cyan-400 h-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {statusMessage && (
        <div className="p-4 rounded-xl bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs flex items-start gap-2.5">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">{statusMessage}</p>
          </div>
        </div>
      )}

      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-start gap-2.5">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">{errorMessage}</p>
          </div>
        </div>
      )}
    </div>
  );
};
