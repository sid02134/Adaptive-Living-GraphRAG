import axios from 'axios';

// Get base URL from environment or default to local FastAPI server
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 45000, // 45 seconds timeout for LLM / ingestion operations
});

// Response interceptor for unified error formatting
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    let errorMessage = 'An unexpected network error occurred.';
    if (error.response) {
      errorMessage = error.response.data?.detail || error.response.data?.message || `Server returned status ${error.response.status}`;
    } else if (error.request) {
      errorMessage = 'Unable to connect to the backend server. Please verify FastAPI is running at ' + API_BASE_URL;
    } else {
      errorMessage = error.message;
    }
    return Promise.reject(new Error(errorMessage));
  }
);

export default api;
