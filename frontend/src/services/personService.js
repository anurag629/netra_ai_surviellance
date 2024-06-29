import api from './api';

export const getPersons = async () => {
  const response = await api.get('/persons');  // Ensure this is a GET request
  return response.data;
};

export const addPerson = async (person) => {
  const response = await api.post('/persons', person);
  return response.data;
};

export const uploadPersonImage = async (personId, imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  const response = await api.post(`/persons/${personId}/upload_image`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data;
};

export const deletePerson = async (personId) => {
  const response = await api.delete(`/persons/${personId}`);
  return response.data;
};
