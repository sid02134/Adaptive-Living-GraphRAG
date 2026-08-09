import api from './api';

export const askQuestion = async (query, topK = 5, alpha = 0.6) => {
  return await api.post('/ask', {
    query,
    top_k: topK,
    alpha: alpha,
  });
};
