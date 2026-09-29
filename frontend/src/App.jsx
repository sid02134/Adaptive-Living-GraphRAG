import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import { Layout } from './components/Layout/Layout';

import { Dashboard } from './pages/Dashboard';
import { Documents } from './pages/Documents';
import { AIChat } from './pages/AIChat';
import { KnowledgeGraph } from './pages/KnowledgeGraph';
import { KnowledgeEvolution } from './pages/KnowledgeEvolution';
import { TrustDashboard } from './pages/TrustDashboard';
import { Analytics } from './pages/Analytics';
import { Settings } from './pages/Settings';
import { About } from './pages/About';

function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/chat" element={<AIChat />} />
            <Route path="/graph" element={<KnowledgeGraph />} />
            <Route path="/evolution" element={<KnowledgeEvolution />} />
            <Route path="/trust" element={<TrustDashboard />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AppProvider>
  );
}

export default App;
