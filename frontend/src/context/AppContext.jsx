import React, { createContext, useContext, useState, useEffect } from 'react';
import { getHealthStatus } from '../services/healthService';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [health, setHealth] = useState({
    status: 'checking',
    components: {
      api: { status: 'checking', details: 'Connecting...' },
      chromadb: { status: 'checking', details: 'Connecting...' },
      neo4j: { status: 'checking', details: 'Connecting...' },
      ollama: { status: 'checking', details: 'Connecting...' },
    },
  });
  const [healthLoading, setHealthLoading] = useState(true);

  // System settings state
  const [settings, setSettings] = useState({
    topK: 5,
    alpha: 0.6,
    temperature: 0.2,
    chunkSize: 500,
    chunkOverlap: 100,
    llmModel: 'Llama 3',
    backendUrl: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000',
  });

  // Recent documents list stored in state
  const [uploadedDocuments, setUploadedDocuments] = useState([
    {
      id: 'doc-1',
      filename: 'GraphRAG_Architecture_Doc.pdf',
      chunks_processed: 18,
      entities_extracted: 42,
      upload_date: new Date().toISOString(),
      status: 'Indexed',
    },
  ]);

  const refreshHealth = async () => {
    setHealthLoading(true);
    try {
      const data = await getHealthStatus();
      setHealth(data);
    } catch (err) {
      setHealth({
        status: 'degraded',
        components: {
          api: { status: 'offline', details: err.message },
          chromadb: { status: 'unknown', details: 'Backend offline' },
          neo4j: { status: 'unknown', details: 'Backend offline' },
          ollama: { status: 'unknown', details: 'Backend offline' },
        },
      });
    } finally {
      setHealthLoading(false);
    }
  };

  useEffect(() => {
    refreshHealth();
    // Auto refresh health every 30 seconds
    const interval = setInterval(refreshHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const addDocument = (docInfo) => {
    const newDoc = {
      id: `doc-${Date.now()}`,
      filename: docInfo.filename,
      chunks_processed: docInfo.chunks_processed || 0,
      entities_extracted: docInfo.entities_extracted || 0,
      upload_date: new Date().toISOString(),
      status: 'Indexed',
    };
    setUploadedDocuments((prev) => [newDoc, ...prev]);
  };

  return (
    <AppContext.Provider
      value={{
        health,
        healthLoading,
        refreshHealth,
        settings,
        setSettings,
        uploadedDocuments,
        addDocument,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
