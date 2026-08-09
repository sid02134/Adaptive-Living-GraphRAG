import api from './api';

export const getDashboardStats = async () => {
  return await api.get('/dashboard');
};

export const getTrustBreakdown = async () => {
  return await api.get('/trust');
};
