import api from './api';

export const getCameras = async () => {
  const response = await api.get('/cameras');
  return response.data;
};

export const addCamera = async (camera) => {
  const response = await api.post('/cameras', camera);
  return response.data;
};

export const deleteCamera = async (id) => {
  const response = await api.delete(`/cameras/${id}`);
  return response.data;
}