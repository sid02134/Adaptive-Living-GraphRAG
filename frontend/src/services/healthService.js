import api from './api';

export const getHealthStatus = async () => {
  return await api.get('/health');
};
