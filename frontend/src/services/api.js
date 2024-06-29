import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      console.error('API error:', error.response.data);
    } else if (error.request) {
      console.error('No response from API:', error.request);
    } else {
      console.error('API request error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
