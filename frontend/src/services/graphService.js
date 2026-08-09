import api from './api';

export const getKnowledgeGraph = async (queryEntity = '') => {
  const params = queryEntity ? { query_entity: queryEntity } : {};
  return await api.get('/graph', { params });
};
