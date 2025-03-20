import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
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