import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const accountsAPI = {
  list: (filters) => api.get('/api/accounts', { params: filters }),
  get: (id) => api.get(`/api/accounts/${id}`),
  create: (data) => api.post('/api/accounts', data),
  update: (id, data) => api.patch(`/api/accounts/${id}`, data),
  delete: (id) => api.delete(`/api/accounts/${id}`),
};

export const postsAPI = {
  list: (filters) => api.get('/api/posts', { params: filters }),
  get: (id) => api.get(`/api/posts/${id}`),
  create: (data) => api.post('/api/posts', data),
  generate: (data) => api.post('/api/posts/generate', data),
  publish: (id) => api.post(`/api/posts/${id}/publish`),
  getAnalytics: (id) => api.get(`/api/posts/${id}/analytics`),
};

export const analyticsAPI = {
  getAccountAnalytics: (accountId, days) =>
    api.get(`/api/analytics/account/${accountId}`, { params: { days } }),
  getPlatformAnalytics: (platform, days) =>
    api.get(`/api/analytics/platform/${platform}`, { params: { days } }),
  getInsights: (filters) => api.get('/api/analytics/insights', { params: filters }),
  sync: (filters) => api.post('/api/analytics/sync', {}, { params: filters }),
};

export default api;
