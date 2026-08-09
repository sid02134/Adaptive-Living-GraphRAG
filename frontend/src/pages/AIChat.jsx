import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Trash2, Sparkles, ShieldCheck, Cpu } from 'lucide-react';
import { askQuestion } from '../services/chatService';
import { ChatMessage } from '../components/ChatMessage/ChatMessage';
import { ChatInput } from '../components/ChatInput/ChatInput';
import { ErrorCard } from '../components/ErrorState/ErrorCard';

export const AIChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome-msg',
      sender: 'bot',
      answer:
        'Hello! I am your **Adaptive Living GraphRAG Assistant**. Ask me any question based on your ingested PDF documents. I will retrieve context chunks from **ChromaDB**, verify entity triples in **Neo4j**, evaluate trust metrics, and synthesize an answer using **Llama 3**.',
      markdown_response:
        'Hello! I am your **Adaptive Living GraphRAG Assistant**.\n\nAsk me any question based on your ingested PDF documents. I will retrieve context chunks from **ChromaDB**, verify entity triples in **Neo4j**, evaluate trust metrics, and synthesize an answer using **Llama 3**.',
      trust_score: 0.92,
      trust_percentage: 92.0,
      confidence_level: 'High Confidence',
      processing_time_ms: 120.0,
      citations: [],
      sources: [],
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSendMessage = async (queryText, topK, alpha) => {
    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: queryText,
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const response = await askQuestion(queryText, topK, alpha);

      const botMsg = {
        id: `bot-${Date.now()}`,
        sender: 'bot',
        query: response.query,
        answer: response.answer,
        markdown_response: response.markdown_response,
        trust_score: response.trust_score,
        trust_percentage: response.trust_percentage,
        confidence_level: response.confidence_level,
        trust_breakdown: response.trust_breakdown,
        citations: response.citations || [],
        sources: response.sources || [],
        processing_time_ms: response.processing_time_ms,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setError(err.message || 'Failed to process question. Please ensure FastAPI and Ollama are active.');
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 'welcome-msg',
        sender: 'bot',
        answer: 'Chat cleared. Ask a new research question to start retrieval.',
        markdown_response: 'Chat cleared. Ask a new research question to start retrieval.',
        trust_score: 0.9,
        trust_percentage: 90.0,
        confidence_level: 'High Confidence',
        processing_time_ms: 50.0,
        citations: [],
        sources: [],
      },
    ]);
    setError(null);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-7rem)] max-w-5xl mx-auto">
      {/* Top Workspace Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800 shrink-0">
        <div>
          <h2 className="text-xl font-extrabold text-slate-100 tracking-tight flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-cyan-400" />
            GraphRAG RAG Assistant Workspace
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Powered by ChromaDB Vector Search, Neo4j Entity Triples, and Ollama Llama 3
          </p>
        </div>

        <button
          onClick={handleClearChat}
          className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700 text-xs flex items-center gap-1.5 transition-colors"
          title="Clear Conversation History"
        >
          <Trash2 className="w-4 h-4 text-rose-400" />
          <span className="hidden sm:inline">Clear Chat</span>
        </button>
      </div>

      {/* Messages Thread Container */}
      <div className="flex-1 overflow-y-auto py-4 px-1 space-y-4">
        {messages.map((msg) => (
          <ChatMessage key={msg.id} message={msg} />
        ))}

        {loading && (
          <div className="flex gap-3 my-6 animate-pulse">
            <div className="w-9 h-9 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-center text-cyan-400">
              <Cpu className="w-5 h-5 animate-spin" />
            </div>
            <div className="flex-1 glass-panel rounded-2xl p-4 border border-slate-800 text-xs text-cyan-300 font-mono flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400 animate-spin" />
              <span>Executing hybrid retrieval, Neo4j graph alignment, and Llama 3 synthesis...</span>
            </div>
          </div>
        )}

        {error && <ErrorCard title="Query Processing Failed" message={error} />}

        <div ref={messagesEndRef} />
      </div>

      {/* Sticky Bottom Input Bar */}
      <div className="pt-2 border-t border-slate-800/80 shrink-0">
        <ChatInput onSendMessage={handleSendMessage} loading={loading} />
      </div>
    </div>
  );
};
