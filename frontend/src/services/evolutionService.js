import api from './api';

export const evolutionService = {
  // Submit new claim/fact for evolution evaluation
  updateKnowledge: async (payload) => {
    return await api.post('/evolution/update', payload);
  },

  // Submit manual conflict resolution feedback
  resolveConflictFeedback: async (conflictId, winningClaimId, rationale = '') => {
    return await api.post('/evolution/feedback', {
      conflict_id: conflictId,
      winning_claim_id: winningClaimId,
      rationale: rationale,
    });
  },

  // Fetch evolution audit history log
  getHistory: async (limit = 50) => {
    return await api.get(`/evolution/history?limit=${limit}`);
  },

  // Fetch all flagged knowledge conflicts
  getConflicts: async () => {
    return await api.get('/evolution/conflicts');
  },

  // Fetch Module 6 system status & config metrics
  getStatus: async () => {
    return await api.get('/evolution/status');
  },

  // Execute 4-Factor Adaptive Retrieval query
  adaptiveQuery: async (payload) => {
    return await api.post('/evolution/query', payload);
  },
};
