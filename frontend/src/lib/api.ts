import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  headers: {
    'Accept': 'application/json',
  },
  withCredentials: false,
});

// Add this line for debugging
console.log('API URL:', process.env.NEXT_PUBLIC_API_URL);

// Add request interceptor to handle different content types
api.interceptors.request.use((config) => {
  // Don't set Content-Type for FormData (browser will set it automatically with boundary)
  if (config.data instanceof FormData) {
    delete config.headers['Content-Type'];
  } else {
    config.headers['Content-Type'] = 'application/json';
  }
  return config;
});

export const uploadPDF = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData);
  return response.data;
};

export const sendMessage = async (message: string) => {
  const response = await api.post('/chat', null, {
    params: { question: message },
  });
  return response.data;
};

export default api;